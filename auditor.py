# auditor.py
# Smart Inventory Auditor

def run_inventory_auditor():
    # Initialize state variables
    inventory = 0
    total_processed = 0
    failed_entries = 0
    
    print("Instructions: Enter stock quantities one by one.")
    print("Type 'quit' to exit and view the report.\n")
    
    while True:
        # Get input from the user
        user_input = input("Enter stock quantity: ").strip()
        
        # Check if the user wants to quit
        if user_input.lower() == 'quit':
            print("\nExiting audit session...")
            break
            
        # Handle invalid inputs (strings, symbols, empty inputs) using .isdigit()
        # Note: .isdigit() evaluates to False for letters, symbols, and negative signs (-)
        if not user_input.isdigit():
            print("Error: ENTER A WHOLE NUMBER.")
            failed_entries += 1
            continue
            
        # Convert valid digit string to an integer
        quantity = int(user_input)
        
        # Enforce business rules (Reject negative numbers, though .isdigit() already filters negatives)
        if quantity < 0:
            print("Error: DO NOT INPUT NEGATIVE NUMBERS.")
            failed_entries += 1
            continue
            
        # Manage State: Update running totals
        inventory += quantity
        total_processed += quantity
        
        # Trigger Overstock Alert (If total inventory exceeds 500 units)
        if inventory > 500:
            print(f"\n INVENTORY IS OVERSTOCKED! ")
            print(f"Total inventory has reached {inventory} units, exceeding the 500-unit limit.")
            print("Emergency shutdown: Breaking the audit loop immediately.")
            break
        else:
            print(f"✔ Success. Current Inventory Total: {inventory} units.\n")
            
    # Final Reporting
    print("FINAL INVENTORY REPORT")
    print(f"Total Units Processed           : {total_processed}")
    print(f"Number of Failed/Rejected Entries: {failed_entries}")
    print(f"Final Inventory Status          : {inventory} units")

if __name__ == "__main__":
    run_inventory_auditor()