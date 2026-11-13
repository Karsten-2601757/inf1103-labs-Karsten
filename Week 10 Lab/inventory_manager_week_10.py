from digital_product import DigitalProduct
from inventory import Inventory
from order import Order
from physical_product import PhysicalProduct
from product import Product
from storage import load_data, save_data
from supplier import Supplier


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
    product_type = input("Choose product type: ").strip()
    if product_type not in ("1", "2"):
        print("Invalid product type.\n")
        return

    product_id = input("Product ID: ").strip()
    if inventory.find_product(product_id) is not None:
        print("Error: Product ID already exists!\n")
        return

    name = input("Product Name: ").strip()
    try:
        price = float(input("Price: "))
        stock = int(input("Stock Quantity: "))
        if product_type == "1":
            weight = float(input("Weight (kg): "))
        else:
            download_size = float(input("Download size (MB): "))
    except ValueError:
        print("Invalid numerical input. Product creation failed.\n")
        return

    supplier = choose_supplier(suppliers)
    if supplier is None:
        print("Product creation failed.\n")
        return

    try:
        product: Product
        if product_type == "1":
            product = PhysicalProduct(product_id, name, price, stock, supplier, weight)
        else:
            product = DigitalProduct(product_id, name, price, stock, supplier, download_size)
    except ValueError:
        print("Values cannot be negative. Product creation failed.\n")
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
    try:
        quantity = int(input("New Stock Quantity: "))
    except ValueError:
        print("Invalid stock input.\n")
        return

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

    print()
    order.display_information()
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
        print("9. Exit")

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