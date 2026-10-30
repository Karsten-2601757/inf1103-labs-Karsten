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
        return cls(data["id"], data["name"], data["price"], data["stock"])

class Inventory:
    """Manages a collection of Product objects."""

    def __init__(self):
        self.__products = []

    def add_product(self, product):
        if self.search_product(product.get_product_id()) is not None:
            return False
        self.__products.append(product)
        return True

    def search_product(self, product_id):
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
        return [product.to_dict() for product in self.__products]
    
def load_inventory():
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

def add_product_menu(inventory):
    print("\nAdd New Product")
    product_id = input("Product ID: ").strip()

    if inventory.search_product(product_id) is not None:
        print("Error: Product ID already exists!\n")
        return

    name = input("Product Name: ").strip()
    try:
        price = float(input("Price: "))
        stock = int(input("Stock Quantity: "))
    except ValueError:
        print("Invalid numerical input. Product creation failed.\n")
        return

    if price < 0 or stock < 0:
        print("Price and stock cannot be negative. Product creation failed.\n")
        return

    inventory.add_product(Product(product_id, name, price, stock))
    print("Product added successfully!\n")


def update_stock_menu(inventory):
    print("\nUpdate Stock")
    product_id = input("Enter Product ID: ").strip()
    product = inventory.search_product(product_id)

    if product is None:
        print("Error, Product not found.\n")
        return

    print(f"\nProduct Found:\nName: {product.get_name()}\n"
          f"Current Stock: {product.get_stock()}\n")
    try:
        quantity = int(input("New Stock Quantity: "))
    except ValueError:
        print("Invalid stock input.\n")
        return

    if product.update_stock(quantity):
        print("Stock updated successfully!\n")
    else:
        print("Invalid stock input. Stock cannot be negative.\n")


def search_product_menu(inventory):
    print("\nSearch Product")
    product_id = input("Enter Product ID: ").strip()
    product = inventory.search_product(product_id)

    if product is None:
        print("Error, Product not found.\n")
        return

    print("\nProduct Found")
    print("-" * 40)
    product.display_information()
    print("-" * 40 + "\n")

def main():
    print("INVENTORY MANAGEMENT SYSTEM")
    inventory = load_inventory()

    while True:
        print("MENU")
        print("1. Display All Products")
        print("2. Add Product")
        print("3. Update Stock")
        print("4. Search Product")
        print("5. Save Inventory")
        print("6. Exit")

        option = input("Enter option: ").strip()

        if option == "1":
            inventory.display_all()
        elif option == "2":
            add_product_menu(inventory)
        elif option == "3":
            update_stock_menu(inventory)
        elif option == "4":
            search_product_menu(inventory)
        elif option == "5":
            save_inventory(inventory)
        elif option == "6":
            print("\nSaving inventory before exit...")
            save_inventory(inventory, show_message=False)
            print("Inventory saved.\n")
            print("Thank you for using Inventory Management System.")
            print("Program terminated.")
            break
        else:
            print("Invalid option. Please try again.\n")


if __name__ == "__main__":
    main()