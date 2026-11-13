import json
import os

from digital_product import DigitalProduct
from inventory import Inventory
from physical_product import PhysicalProduct
from product import Product
from supplier import Supplier

FILENAME: str = "inventory.json"

# Maps the saved "type" to the class that rebuilds it.
PRODUCT_TYPES: dict[str, type[PhysicalProduct] | type[DigitalProduct]] = {
    "physical": PhysicalProduct,
    "digital": DigitalProduct,
}

# Used when an old (Week 9) inventory.json has no supplier information.
UNKNOWN_SUPPLIER_ID: str = "UNKNOWN"


def product_from_dict(data: dict, suppliers: dict[str, Supplier]) -> Product:
    product_type = data.get("type")
    if product_type not in PRODUCT_TYPES:
        raise ValueError(f"Unknown product type: {product_type}")

    supplier_id = data.get("supplier_id", UNKNOWN_SUPPLIER_ID)
    if supplier_id not in suppliers:
        if supplier_id != UNKNOWN_SUPPLIER_ID:
            raise ValueError(f"Unknown supplier: {supplier_id}")
        suppliers[supplier_id] = Supplier(UNKNOWN_SUPPLIER_ID,
                                          "Unknown supplier", "n/a")
    return PRODUCT_TYPES[product_type].from_dict(data, suppliers[supplier_id])


def load_data() -> tuple[Inventory, dict[str, Supplier]]:
    """Return the inventory and the supplier registry (id -> Supplier)."""
    inventory = Inventory()
    suppliers: dict[str, Supplier] = {}

    if os.path.exists(FILENAME):
        try:
            with open(FILENAME, "r") as file:
                data = json.load(file)

            # Old format was just a list of products.
            if isinstance(data, list):
                data = {"suppliers": [], "products": data}

            for item in data["suppliers"]:
                supplier = Supplier.from_dict(item)
                suppliers[supplier.get_supplier_id()] = supplier
            for item in data["products"]:
                inventory.add_product(product_from_dict(item, suppliers))

            print("inventory.json found.")
            print("Inventory loaded successfully.\n")
            return inventory, suppliers
        except (json.JSONDecodeError, KeyError, TypeError, ValueError):
            print("Error reading inventory.json. Initializing default inventory.\n")
            return Inventory(), {}

    return inventory, suppliers


def save_data(inventory: Inventory, suppliers: dict[str, Supplier],
              show_message: bool = True) -> None:
    if show_message:
        print("Saving inventory...")
    data = {
        "suppliers": [s.to_dict() for s in suppliers.values()],
        "products": inventory.to_list(),
    }
    with open(FILENAME, "w") as file:
        json.dump(data, file, indent=4)
    if show_message:
        print("Inventory saved successfully to inventory.json.\n")