import ast
import inspect
import os
import sys
import tempfile
import unittest
from io import StringIO
from unittest.mock import patch

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import order as order_module
from csv_loader import load_products
from digital_product import DigitalProduct
from discounts import (BulkDiscount, DiscountStrategy, NoDiscount,
                       PercentageDiscount, StudentDiscount)
from input_helpers import get_non_negative_int, get_positive_float
from inventory import Inventory
from order import Order
from physical_product import PhysicalProduct
from product import Product
from product_factory import ProductFactory
from supplier import Supplier

SUPPLIER = Supplier("S1", "Acme", "a@acme.example")
CSV_TEXT = """product_type,product_id,name,price,stock_quantity
physical,P001,Desk Lamp,25.00,10
digital,D001,Photo Editor,49.90,100
service,S001,Installation,30.00,5
physical,P002,Office Chair,abc,3
physical,P003,Monitor Stand,39.50,7
"""


def make_order(discount=None, price=250.0):
    product = ProductFactory.create("physical", "P1", "Thing", price, 10, SUPPLIER, 1.0)
    order = Order("O1", discount)
    order.add_order_line(product, 1)
    return order


def _is_default_discount(node) -> bool:
    """The only allowed conditional: `discount if discount is not None else NoDiscount()`."""
    return isinstance(node, ast.IfExp) and "NoDiscount" in ast.dump(node)


class TestDiscounts(unittest.TestCase):
    def test_default_is_no_discount(self):
        self.assertEqual(make_order().calculate_total(), 250)

    def test_bulk_discount(self):
        self.assertEqual(make_order(BulkDiscount(200, 20)).calculate_total(), 230)

    def test_bulk_below_threshold(self):
        self.assertEqual(make_order(BulkDiscount(200, 20), price=100).calculate_total(), 100)

    def test_percentage_discount(self):
        self.assertAlmostEqual(make_order(PercentageDiscount(10)).calculate_total(), 225)

    def test_set_discount_changes_strategy(self):
        order = make_order(BulkDiscount(200, 20))
        self.assertEqual(order.calculate_total(), 230)
        order.set_discount(PercentageDiscount(10))
        self.assertAlmostEqual(order.calculate_total(), 225)

    def test_new_strategy_needs_no_order_change(self):
        self.assertIsInstance(StudentDiscount(), DiscountStrategy)
        self.assertAlmostEqual(make_order(StudentDiscount()).calculate_total(), 237.5)

    def test_order_has_no_discount_branching(self):
        tree = ast.parse(inspect.getsource(order_module.Order))
        branches_on_discount = any(
            isinstance(node, (ast.If, ast.IfExp)) and
            "discount" in ast.dump(node.test).lower() and
            not _is_default_discount(node)
            for node in ast.walk(tree))
        self.assertFalse(branches_on_discount,
                         "Order must not branch on discount type")

    def test_strategies_inherit_base(self):
        for cls in (NoDiscount, PercentageDiscount, BulkDiscount, StudentDiscount):
            self.assertTrue(issubclass(cls, DiscountStrategy))

    def test_bad_percentage_rejected(self):
        for bad in (-1, 101):
            with self.assertRaises(ValueError):
                PercentageDiscount(bad)


class TestFactory(unittest.TestCase):
    def test_creates_physical(self):
        p = ProductFactory.create("physical", "P1", "A", 5.0, 1, SUPPLIER, 2.0)
        self.assertIsInstance(p, PhysicalProduct)
        self.assertIsInstance(p, Product)
        self.assertEqual(p.get_weight(), 2.0)

    def test_creates_digital(self):
        p = ProductFactory.create("digital", "D1", "B", 5.0, 1, SUPPLIER, 300.0)
        self.assertIsInstance(p, DigitalProduct)
        self.assertEqual(p.get_download_size(), 300.0)

    def test_unknown_type_raises_clear_message(self):
        with self.assertRaises(ValueError) as ctx:
            ProductFactory.create("service", "S1", "C", 5.0, 1, SUPPLIER)
        self.assertEqual(str(ctx.exception), "Unknown product type: service")

    def test_create_from_dict_round_trip(self):
        original = ProductFactory.create("digital", "D1", "B", 5.0, 3, SUPPLIER, 12.5)
        rebuilt = ProductFactory.create_from_dict(original.to_dict(), SUPPLIER)
        self.assertIsInstance(rebuilt, DigitalProduct)
        self.assertEqual(rebuilt.to_dict(), original.to_dict())

    def test_create_from_dict_unknown_type(self):
        with self.assertRaises(ValueError):
            ProductFactory.create_from_dict({"type": "service"}, SUPPLIER)


class TestValidation(unittest.TestCase):
    def test_price_must_be_positive(self):
        for bad in (0, -1):
            for kind in ("physical", "digital"):
                with self.assertRaises(ValueError):
                    ProductFactory.create(kind, "P", "A", bad, 1, SUPPLIER)

    def test_stock_cannot_be_negative(self):
        with self.assertRaises(ValueError):
            ProductFactory.create("digital", "D", "A", 5, -1, SUPPLIER)

    def test_zero_stock_allowed(self):
        p = ProductFactory.create("digital", "D", "A", 5, 0, SUPPLIER)
        self.assertEqual(p.get_stock(), 0)

    def test_update_stock_rejects_negative(self):
        p = ProductFactory.create("digital", "D", "A", 5, 3, SUPPLIER)
        self.assertFalse(p.update_stock(-5))
        self.assertEqual(p.get_stock(), 3)

    def test_order_line_quantity_must_be_positive(self):
        p = ProductFactory.create("physical", "P", "A", 5, 1, SUPPLIER)
        order = Order("O")
        for bad in (0, -2):
            with self.assertRaises(ValueError):
                order.add_order_line(p, bad)


class TestInputHandling(unittest.TestCase):
    def test_reprompts_until_valid(self):
        with patch("builtins.input", side_effect=["abc", "-5", "12.50"]), \
                patch("sys.stdout", new_callable=StringIO) as out:
            value = get_positive_float("Price: ")
        self.assertEqual(value, 12.50)
        lines = out.getvalue().strip().splitlines()
        self.assertEqual(lines, ["Please enter a valid number, e.g. 12.50",
                                 "Please enter a number greater than zero."])

    def test_non_negative_int_accepts_zero(self):
        with patch("builtins.input", side_effect=["x", "-1", "2.5", "0"]), \
                patch("sys.stdout", new_callable=StringIO):
            self.assertEqual(get_non_negative_int("Stock: "), 0)


class TestLoadProducts(unittest.TestCase):
    def test_missing_file(self):
        inv = Inventory()
        with patch("sys.stdout", new_callable=StringIO) as out:
            loaded = load_products("does_not_exist.csv", inv, SUPPLIER)
        self.assertEqual(loaded, 0)
        text = out.getvalue()
        self.assertIn("Products file not found", text)
        self.assertIn("Load attempt finished.", text)
        self.assertNotIn("products loaded", text)

    def test_bad_rows_skipped_valid_rows_load(self):
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "products.csv")
            with open(path, "w", newline="") as f:
                f.write(CSV_TEXT)
            inv = Inventory()
            with patch("sys.stdout", new_callable=StringIO) as out:
                loaded = load_products(path, inv, SUPPLIER)
        self.assertEqual(loaded, 3)
        self.assertEqual([p.get_product_id() for p in inv.products],
                         ["P001", "D001", "P003"])
        text = out.getvalue()
        self.assertIn("Unknown product type: service", text)
        self.assertIn("could not convert string to float", text)
        self.assertLess(text.index("3 products loaded."),
                        text.index("Load attempt finished."))


if __name__ == "__main__":
    unittest.main()