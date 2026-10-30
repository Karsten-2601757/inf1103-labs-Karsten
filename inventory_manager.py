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
    """Loads inventory data from inventory.json if it exists, otherwise initializes default items."""
    if os.path.exists(FILENAME):
        try:
            with open(FILENAME, "r") as file:
                print("inventory.json found.")
                print("Inventory loaded successfully.\n")
                return json.load(file)
        except json.JSONDecodeError:
            print("Error reading inventory.json. Initializing default inventory.\n")
    
    return [
        {"id": "P001", "name": "Laptop", "price": 1200.00, "stock": 15},
        {"id": "P002", "name": "Mouse", "price": 25.50, "stock": 40},
        {"id": "P003", "name": "Keyboard", "price": 45.00, "stock": 25}
    ]

def save_inventory(inventory, show_message=True):
    """Saves inventory data to inventory.json."""
    if show_message:
        print("Saving inventory...")
    with open(FILENAME, "w") as file:
        json.dump(inventory, file, indent=4)
    if show_message:
        print("Inventory saved successfully to inventory.json.\n")

def display_all(inventory):
    print("\nCurrent Inventory")
    if not inventory:
        print("No products available.\n")
        return
    for item in inventory:
        print(f"ID: {item['id']} | Name: {item['name']} | Price: ${item['price']:.2f} | Stock: {item['stock']}")
    print()

def add_product(inventory):
    print("\nAdd New Product")
    product_id = input("Product ID: ").strip()
    
    for item in inventory:
        if item["id"].upper() == product_id.upper():
            print("Error: Product ID already exists!\n")
            return

    name = input("Product Name: ").strip()
    try:
        price = float(input("Price: "))
        stock = int(input("Stock Quantity: "))
    except ValueError:
        print("Invalid numerical input. Product creation failed.\n")
        return

    inventory.append({"id": product_id, "name": name, "price": price, "stock": stock})
    print("Product added successfully!\n")

def update_stock(inventory):
    print("\nUpdate Stock")
    product_id = input("Enter Product ID: ").strip()
    for item in inventory:
        if item["id"].upper() == product_id.upper():
            print(f"\nProduct Found:\nName: {item['name']}\nCurrent Stock: {item['stock']}\n")
            try:
                item["stock"] = int(input("New Stock Quantity: "))
                print("Stock updated successfully!\n")
            except ValueError:
                print("Invalid stock input.\n")
            return
    print("Error, Product not found.\n")

def search_product(inventory):
    print("\nSearch Product")
    product_id = input("Enter Product ID: ").strip()
    for item in inventory:
        if item["id"].upper() == product_id.upper():
            print("\nProduct Found")
            print("-" * 40)
            print(f"ID: {item['id']}\nName: {item['name']}\nPrice: ${item['price']:.2f}\nStock: {item['stock']}")
            print("-" * 40 + "\n")
            return
    print("Error, Product not found.\n")

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
            display_all(inventory)
        elif option == "2":
            add_product(inventory)
        elif option == "3":
            update_stock(inventory)
        elif option == "4":
            search_product(inventory)
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