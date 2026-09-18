# auditor.py
# Smart Inventory Auditor
inventory = 0 
fails = 0

def get_valid_input():
    user_input = input("Please enter a valid integer (Type quit to exit):")
    if user_input.lower == "quit": 
        return "quit"
     
    elif user_input.isdigit:
        return int(user_input)
    
    else:
        print("Please input a valid non-negative integer.")
        return "none"

def process_delivery(current_total, new_value):
    return current_total + new_value

def calculate_tax(amount):
    return amount * 0.1

