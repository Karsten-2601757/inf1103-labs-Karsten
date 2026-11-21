import json
import os
from inventory import Inventory
from product import Product
from product_factory import ProductFactory
from supplier import Supplier
FILENAME: str = "inventory.json"
UNKNOWN_SUPPLIER_ID: str = "UNKNOWN"
def product_from_dict(data: dict, suppliers: dict[str, Supplier]) -> Product:
    supplier_id = data.get("supplier_id", UNKNOWN_SUPPLIER_ID)
    if supplier_id not in suppliers:
        if supplier_id != UNKNOWN_SUPPLIER_ID:
            raise ValueError(f"Unknown supplier: {supplier_id}")
        suppliers[supplier_id] = Supplier(UNKNOWN_SUPPLIER_ID,
                                          "Unknown supplier", "n/a")
    return ProductFactory.create_from_dict(data, suppliers[supplier_id])
 
def load_data() -> tuple[Inventory, dict[str, Supplier]]:
    """Return the inventory and the supplier registry (id -> Supplier)."""
    inventory = Inventory()
    suppliers: dict[str, Supplier] = {}
    if os.path.exists(FILENAME):
        try:
            with open(FILENAME, "r") as file:
                data = json.load(file)
            if isinstance(data, list):
                data = {"suppliers": [], "products": data}
            for item in data["suppliers"]:
                supplier = Supplier.from_dict(item)
                suppliers[supplier.get_supplier_id()] = supplier
            for item in data["products"]:
                try:
                    inventory.add_product(product_from_dict(item, suppliers))
                except (ValueError, KeyError) as error:
                    print(f"Skipping invalid product in inventory.json: {error}")
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