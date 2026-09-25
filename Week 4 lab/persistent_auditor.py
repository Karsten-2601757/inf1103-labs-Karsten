# persistent_auditor.py
import os

def load_orders(filename="orders.txt"):
    """Loads existing orders from file and returns the list of lines."""
    orders = []
    print("Current Orders:\n")
    if os.path.exists(filename):
        with open(filename, "r") as f:
            for line in f:
                line = line.strip()
                if line:
                    orders.append(line)
                    print(line)
        print()
    return orders

def save_orders(orders, filename="orders.txt"):
    """Saves all orders to file."""
    with open(filename, "w") as f:
        for order in orders:
            f.write(f"{order}\n")
    print(f"\nOrder successfully saved to {filename}")

def calculate_tax(amount):
    return amount * 0.1

def generate_report(total_units, failed_attempts, total_tax):
    print("\n--- Final Summary ---")
    print("Total number of failed entries:", failed_attempts)
    print("Total inventory processed:", total_units)
    print(f"Total tax calculated: {total_tax:.2f}")

# --- MAIN EXECUTION ---
orders_list = load_orders()

# State variables
next_id = 1001 + len(orders_list)
total_inventory = 0
total_tax = 0.0
fails = 0

while True:
    product_name = input("Enter Product Name (or type 'quit' to exit): ").strip()
    
    if product_name.lower() == "quit":
        save_orders(orders_list)
        break
        
    quantity_input = input("Enter Quantity: ").strip()
    
    # Input validation for quantity
    if quantity_input.isdigit():
        quantity = int(quantity_input)
        
        # Calculate totals
        total_inventory += quantity
        tax = calculate_tax(quantity)
        total_tax += tax
        
        # Format order entry
        new_order = f"{next_id}, {product_name}, {quantity}"
        orders_list.append(new_order)
        
        print("\nNew Order Added:")
        print(new_order)
        print(f"Tax for this item: {tax:.2f}")
        print(f"Current Total Inventory: {total_inventory}\n")
        
        next_id += 1
    else:
        print("Invalid quantity entered. Entry rejected.\n")
        fails += 1

generate_report(total_inventory, fails, total_tax)