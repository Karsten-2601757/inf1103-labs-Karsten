
from digital_product import DigitalProduct
from physical_product import PhysicalProduct
from product import Product
from supplier import Supplier

EXTRA_FIELDS: dict[str, str] = {
    "physical": "weight",
    "digital": "download_size",
}

class ProductFactory:
    @staticmethod
    def create(product_type: str, product_id: str, name: str, price: float,
               stock: int, supplier: Supplier, extra: float = 0.0) -> Product:
        if product_type == "physical":
            return PhysicalProduct(product_id, name, price, stock, supplier, extra)
        elif product_type == "digital":
            return DigitalProduct(product_id, name, price, stock, supplier, extra)
        else:
            raise ValueError(f"Unknown product type: {product_type}")
    @staticmethod
    def create_from_dict(data: dict, supplier: Supplier) -> Product:
        product_type = data.get("type")
        if product_type not in EXTRA_FIELDS:
            raise ValueError(f"Unknown product type: {product_type}")
        return ProductFactory.create(
            product_type, data["id"], data["name"], data["price"],
            data["stock"], supplier, data[EXTRA_FIELDS[product_type]])