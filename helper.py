"""helpers.py - Utility functions for input parsing and transaction creation."""

__all__ = ["get_transaction_info", "get_currency_input", "clear_screen", "get_item_info", "transaction"]

from datetime import datetime
import json
import os
from enum import Enum
import inventory

class Rarity(Enum):
    COMMON = "common"
    UNCOMMON = "uncommon"
    RARE = "rare"
    HEROIC = "heroic"
    EPIC = "epic"
    LEGENDARY = "legendary"
    ARTIFACT = "artifact"



### input / output helpers

def is_valid_rarity(value: str) -> bool:
    return value.lower() in (r.value for r in Rarity)

def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def get_currency_input():
    while True:
        try:
            # Get inputs, but allow them to be empty
            gold_input = input("Gold: ").strip()
            silver_input = input("Silver: ").strip()
            copper_input = input("Copper: ").strip()

            # If the input is empty, set it to 0
            gold_input = int(gold_input) if gold_input else 0
            silver_input = int(silver_input) if silver_input else 0
            copper_input = int(copper_input) if copper_input else 0

            # Ensure no negative numbers
            if gold_input < 0 or silver_input < 0 or copper_input < 0:
                print("Amounts cannot be negative. Please enter valid values.")
                continue

            # Convert everything into copper
            copper_total = gold_input * 10000 + silver_input * 100 + copper_input
            return copper_total
        except ValueError:
            print("Invalid input. Please enter numeric values for gold, silver, and copper.")

def get_item_info(quantity_needed=False):
    item = input("Item name: ")
    while True:
        rarity = input("Enter rarity: ").strip().lower()
        if is_valid_rarity(rarity):
            break
        print("Invalid rarity. Please enter a valid rarity.")
    
    if quantity_needed:
        quantity = get_int_input("Quantity: ")
        return item, rarity, quantity
    
    return item, rarity

def get_transaction_info(username, transaction_type):
    counterparty = input("Enter counterparty (optional): ").strip()
    transaction_amount = get_currency_input()
    notes = input("Enter notes (optional): ").strip()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return {
        'username': username,
        'counterparty': counterparty or "N/A",
        'transaction_amount': transaction_amount if isinstance(transaction_amount, int) else 0,
        'transaction_type': transaction_type,
        'notes': notes or "",
        'timestamp': timestamp
    }

def get_int_input(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Please enter a valid number.")

def get_user_info(config_path="config.json"):
    if os.path.exists(config_path):
        with open(config_path, "r") as f:
            config = json.load(f)
            if "username" in config:
                return config["username"]
    
    username = input("Enter your username: ").strip()
    with open(config_path, "w") as f:
        json.dump({"username": username}, f, indent=2)
    return username

def update_settings(config_path="config.json"):
    if os.path.exists(config_path):
        with open(config_path, "r") as f:
            config = json.load(f)
            
        
        while True:
            print("Current Settings: ")
            for k, v in config.items():
                print(f"    {k}: {v}")
            
            response = input("What line would you like to edit or quit to cancel: ").strip().lower()
            if response in ["quit", "cancel"]:
                break
            
            if response not in config:
                print("Setting doesn't exist")
                continue
            
            updated_info = input(f"New value for {response}: ").strip()
            config[response] = updated_info
            
            with open(config_path, "w") as f:
                json.dump(config, f, indent=2)
                print("Settings updated.")

def create_item_request(username, transaction_type, quantity_needed):
    item, rarity, quantity = get_item_info(quantity_needed=True)
    transaction_info = get_transaction_info(username=username, transaction_type="deposit")
    return {
        "item_name": item,
        "rarity": rarity,
        "quantity_handled": quantity,
        "transaction_info": transaction_info
    }

def print_help_text():
    print("""Commands are:
        \"add item\" or \"add\" or \"deposit\", 
        \"remove item\" or \"remove\" or \"withdraw\", 
        \"check stock\" or \"lookup\" or \"stock\",
        \"edit settings\" or \"settings\",
        \"batch\", 
        \"info\" or \"help\", 
        \"quit\" or \"exit\"""")

### database interaction helpers



def process_inventory_transaction(username, inventory_sheet, transaction_sheet, transaction_type):
    
    if transaction_type.lower() == "deposit":
        requested_item = create_item_request(username=username, transaction_type=transaction_type, quantity_needed=True)
        inventory.add_item(inventory_sheet=inventory_sheet, transaction_sheet=transaction_sheet, requested_item=requested_item)
        print(f"Added {requested_item['item_name']} with rarity: {requested_item['rarity']} and count: {requested_item['quantity_handled']}.")
    else:
        requested_item = create_item_request(username=username, transaction_type=transaction_type, quantity_needed=True)
        result = inventory.remove_item(inventory_sheet=inventory_sheet, transaction_sheet=transaction_sheet, requested_item=requested_item)

        if result == -1:
            print(f"Removed {requested_item['quantity_handled']} {requested_item['item_name']} with rarity {requested_item['rarity']}")
        else:
            print(f"Insufficent stock. {requested_item['item_name']} has {result} in stock.")
    


def transaction():
    print("not implemented")

















