# auditor.py
# Smart Inventory Auditor
inventory = 0 
fails = 0
total_tax = 0

def get_valid_input():
    user_input = input("Please enter a valid integer (Type quit to exit):")
    if user_input.lower() == "quit": 
        return "quit"
     
    elif user_input.isdigit():
        return int(user_input)
    
    else:
        print("Please input a valid non-negative integer.")
        return None

def process_delivery(current_total, new_value):
    return current_total + new_value

def calculate_tax(amount):
    return amount * 0.1

def generate_report(total_units, failed_attempts):
    print("Final Summery")
    print("Total number of failed entries:", failed_attempts)
    print("Total deliveries processed:", total_units)

inventory = 0 
fails = 0
total_tax = 0

while True:
    val = get_valid_input()

    if val == "quit":
        break
    elif val == "None":
        fails = fails + 1
    else:
        inventory = process_delivery(inventory, val)
        tax = calculate_tax(val)
        total_tax = total_tax + tax
        print('Total processed is:', val)
        print("Tax is:", tax)
generate_report(inventory, fails)