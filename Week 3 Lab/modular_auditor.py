# auditor.py
# Smart Inventory Auditor
inventory = 0 
fails = 0

def get_valid_input():
    user_input = input("Please enter a valid integer (Type quit to exit):")
    if user_input.lower == "quit": #if user types in quit, the code will "Break"
        return "quit"
        break 
    elif user_input.isdigit:
        return int(user_input)
    else:
        print("Please input a valid non-negative integer.")
        return "none"