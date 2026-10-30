import json
import os

FILENAME = "inventory.json"

class Product:

    def __init__(self, product_id, name, price, stock):
        self.__product_id = product_id
        self.__name = name
        self.__price = price
        self.__stock = stock

    def get_product_id(self):
        return self.__product_id

    def get_name(self):
        return self.__name

    def get_price(self):
        return self.__price

    def get_stock(self):
        return self.__stock

    def update_stock(self, quantity):
        """Sets the stock to a new quantity. Returns True if accepted."""
        if not isinstance(quantity, int) or quantity < 0:
            return False
        self.__stock = quantity
        return True

    def display_information(self):
        print(f"ID: {self.__product_id} | Name: {self.__name} | "
              f"Price: ${self.__price:.2f} | Stock: {self.__stock}")

    def to_dict(self):
        return {
            "id": self.__product_id,
            "name": self.__name,
            "price": self.__price,
            "stock": self.__stock,
        }

    @classmethod
    def from_dict(cls, data):
        """Creates a Product from a dictionary (used for JSON loading)."""
        return cls(data["id"], data["name"], data["price"], data["stock"])

class Inventory:
    """Manages a collection of Product objects."""

    def __init__(self):
        self.__products = []

    def add_product(self, product):
        """Adds a product. Returns False if the ID already exists."""
        if self.search_product(product.get_product_id()) is not None:
            return False
        self.__products.append(product)
        return True

    def search_product(self, product_id):
        """Returns the matching Product (case-insensitive ID) or None."""
        for product in self.__products:
            if product.get_product_id().upper() == product_id.strip().upper():
                return product
        return None

    def display_all(self):
        print("\nCurrent Inventory")
        if not self.__products:
            print("No products available.\n")
            return
        for product in self.__products:
            product.display_information()
        print()

    def to_list(self):
        """Returns the inventory as a list of dictionaries (for saving)."""
        return [product.to_dict() for product in self.__products]
    
def load_inventory():
    """Loads inventory.json into an Inventory object, or creates defaults."""
    inventory = Inventory()

    if os.path.exists(FILENAME):
        try:
            with open(FILENAME, "r") as file:
                data = json.load(file)
            for item in data:
                inventory.add_product(Product.from_dict(item))
            print("inventory.json found.")
            print("Inventory loaded successfully.\n")
            return inventory
        except (json.JSONDecodeError, KeyError, TypeError):
            print("Error reading inventory.json. Initializing default inventory.\n")
            inventory = Inventory()

    return inventory

def save_inventory(inventory, show_message=True):
    """Saves the Inventory object to inventory.json."""
    if show_message:
        print("Saving inventory...")
    with open(FILENAME, "w") as file:
        json.dump(inventory.to_list(), file, indent=4)
    if show_message:
        print("Inventory saved successfully to inventory.json.\n")