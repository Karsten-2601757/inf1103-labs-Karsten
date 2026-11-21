from csv_loader import load_products
from discounts import (BulkDiscount, DiscountStrategy, NoDiscount,
                       PercentageDiscount, StudentDiscount)
from input_helpers import (get_non_negative_float, get_non_negative_int,
                           get_positive_float)
from inventory import Inventory
from order import Order
from product import Product
from product_factory import ProductFactory
from storage import load_data, save_data
from supplier import Supplier
DISCOUNT_OPTIONS: dict[str, tuple[str, DiscountStrategy]] = {
    "1": ("No discount", NoDiscount()),
    "2": ("10% off", PercentageDiscount(10)),
    "3": ("$20 off orders of $200 or more", BulkDiscount(200, 20)),
    "4": ("Student discount (5% off)", StudentDiscount()),
}
PRODUCT_TYPES: dict[str, str] = {"1": "physical", "2": "digital"}
EXTRA_PROMPTS: dict[str, str] = {
    "physical": "Weight (kg): ",
    "digital": "Download size (MB): ",
}
def show_product_details(product: Product) -> None:
    product.display_information()
    print(f"    {product.get_fulfilment_info()}")

def choose_supplier(suppliers: dict[str, Supplier]) -> Supplier | None:
    print("\nSupplier")
    for supplier in suppliers.values():
        supplier.display_information()
    supplier_id = input("Supplier ID (existing, or a new ID to create one): ").strip()
    if not supplier_id:
        print("Supplier ID cannot be empty.\n")
        return None
    for existing_id, supplier in suppliers.items():
        if existing_id.upper() == supplier_id.upper():
            return supplier
    name = input("New supplier name: ").strip()
    email = input("New supplier contact email: ").strip()
    if not name or not email:
        print("Supplier name and email cannot be empty.\n")
        return None
    supplier = Supplier(supplier_id, name, email)
    suppliers[supplier_id] = supplier
    return supplier

def add_product_menu(inventory: Inventory, suppliers: dict[str, Supplier]) -> None:
    print("\nAdd New Product")
    print("1. Physical product")
    print("2. Digital product")
    choice = input("Choose product type: ").strip()
    if choice not in PRODUCT_TYPES:
        print("Invalid product type.\n")
        return
    product_type = PRODUCT_TYPES[choice]
    product_id = input("Product ID: ").strip()
    if not product_id:
        print("Product ID cannot be empty.\n")
        return
    if inventory.find_product(product_id) is not None:
        print("Error: Product ID already exists!\n")
        return
    name = input("Product Name: ").strip()
    price = get_positive_float("Price: ")
    stock = get_non_negative_int("Stock Quantity: ")
    extra = get_non_negative_float(EXTRA_PROMPTS[product_type])
    supplier = choose_supplier(suppliers)
    if supplier is None:
        print("Product creation failed.\n")
        return
    try:
        product = ProductFactory.create(product_type, product_id, name,
                                        price, stock, supplier, extra)
    except ValueError as error:
        print(f"{error} Product creation failed.\n")
        return
    inventory.add_product(product)
    print("Product added successfully!\n")

def update_stock_menu(inventory: Inventory) -> None:
    print("\nUpdate Stock")
    product = inventory.find_product(input("Enter Product ID: ").strip())
    if product is None:
        print("Error, Product not found.\n")
        return
    print(f"\nProduct Found:\nName: {product.get_name()}\n"
          f"Current Stock: {product.get_stock()}\n")
    quantity = get_non_negative_int("New Stock Quantity: ")
    if product.update_stock(quantity):
        print("Stock updated successfully!\n")
    else:
        print("Invalid stock input. Stock cannot be negative.\n")

def search_product_menu(inventory: Inventory) -> None:
    print("\nSearch Product")
    product = inventory.find_product(input("Enter Product ID: ").strip())
    if product is None:
        print("Error, Product not found.\n")
        return
    print("\nProduct Found")
    print("-" * 40)
    show_product_details(product)
    print("-" * 40 + "\n")

def remove_product_menu(inventory: Inventory) -> None:
    print("\nRemove Product")
    product_id = input("Enter Product ID: ").strip()
    if inventory.remove_product(product_id):
        print("Product removed from the inventory.\n")
    else:
        print("Error, Product not found.\n")

def display_suppliers(suppliers: dict[str, Supplier]) -> None:
    print("\nSuppliers")
    if not suppliers:
        print("No suppliers available.")
    for supplier in suppliers.values():
        supplier.display_information()
    print()

def choose_discount() -> DiscountStrategy:
    print("\nDiscount")
    for key, (label, _) in DISCOUNT_OPTIONS.items():
        print(f"{key}. {label}")
    while True:
        choice = input("Choose discount: ").strip()
        if choice in DISCOUNT_OPTIONS:
            return DISCOUNT_OPTIONS[choice][1]
        print("Please choose one of the numbers listed.")

def create_order_menu(inventory: Inventory) -> None:
    print("\nCreate Order")
    order = Order(input("Order ID: ").strip())
    while True:
        product_id = input("Product ID to add (blank to finish): ").strip()
        if not product_id:
            break
        product = inventory.find_product(product_id)
        if product is None:
            print("Error, Product not found.")
            continue
        try:
            quantity = int(input("Quantity: "))
            order.add_order_line(product, quantity)
        except ValueError:
            print("Quantity must be a positive whole number.")
    order.set_discount(choose_discount())
    print()
    order.display_information()
    print()

def import_products_menu(inventory: Inventory, suppliers: dict[str, Supplier]) -> None:
    print("\nImport Products from CSV")
    path = input("CSV file path (blank for products.csv): ").strip() or "products.csv"
    supplier = choose_supplier(suppliers)
    if supplier is None:
        print("Import cancelled.\n")
        return
    load_products(path, inventory, supplier)
    print()

def main() -> None:
    print("INVENTORY MANAGEMENT SYSTEM")
    inventory, suppliers = load_data()
    while True:
        print("MENU")
        print("1. Display All Products")
        print("2. Add Product")
        print("3. Update Stock")
        print("4. Search Product")
        print("5. Remove Product")
        print("6. Display Suppliers")
        print("7. Create Order")
        print("8. Save Inventory")
        print("9. Import Products from CSV")
        print("10. Exit")
        option = input("Enter option: ").strip()
        if option == "1":
            inventory.display_all_products()
        elif option == "2":
            add_product_menu(inventory, suppliers)
        elif option == "3":
            update_stock_menu(inventory)
        elif option == "4":
            search_product_menu(inventory)
        elif option == "5":
            remove_product_menu(inventory)
        elif option == "6":
            display_suppliers(suppliers)
        elif option == "7":
            create_order_menu(inventory)
        elif option == "8":
            save_data(inventory, suppliers)
        elif option == "9":
            import_products_menu(inventory, suppliers)
        elif option == "10":
            print("\nSaving inventory before exit...")
            save_data(inventory, suppliers, show_message=False)
            print("Inventory saved.\n")
            print("Thank you for using Inventory Management System.")
            print("Program terminated.")
            break
        else:
            print("Invalid option. Please try again.\n")

if __name__ == "__main__":
    main()