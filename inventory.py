""" inventory.py - Functions for manipulating information inside the database. """

QUANTITY_COLUMN_INDEX = 3
RARITY_COLUMN_INDEX = 1

def transaction(transaction_sheet, item_name, rarity, quantity_handled, transaction_info):
    transaction_sheet.append_row(
        [
            item_name,
            rarity,
            quantity_handled,
            transaction_info.get("username"),
            transaction_info.get("counterparty"),
            transaction_info.get("transaction_amount"),
            transaction_info.get("transaction_type"),
            transaction_info.get("notes"),
            transaction_info.get("timestamp")
        ]
    )

def find_row(inventory_sheet, item_name, rarity):
    cells = inventory_sheet.findall(item_name)
    for cell in cells:
        row = inventory_sheet.row_values(cell.row)
        if row[RARITY_COLUMN_INDEX] == rarity:
            return cell.row
    return None

# Next edit add and remove item to handle the dictionary input
def add_item(inventory_sheet, transaction_sheet, requested_item):
    found_row = find_row(inventory_sheet, requested_item["item_name"], requested_item["rarity"])
    if found_row == None:
        inventory_sheet.append_row([requested_item["item_name"], requested_item["rarity"], requested_item["quantity_handled"]])
    else:
        current_quantity = int(inventory_sheet.cell(found_row, QUANTITY_COLUMN_INDEX).value)
        new_quantity = current_quantity + requested_item["quantity_handled"]
        inventory_sheet.update_cell(found_row, QUANTITY_COLUMN_INDEX, new_quantity)
    
    transaction(transaction_sheet, requested_item["item_name"], requested_item["rarity"], requested_item["quantity_handled"], requested_item["transaction_info"])
        
def remove_item(inventory_sheet, transaction_sheet, requested_item):
    found_row = find_row(inventory_sheet, requested_item["item_name"], requested_item["rarity"])
    if found_row == None:
        return 0
    else: 
        current_quantity = int(inventory_sheet.cell(found_row, QUANTITY_COLUMN_INDEX).value)
        if requested_item["quantity_handled"] > current_quantity:
            return current_quantity
        
        new_quantity = current_quantity - requested_item["quantity_handled"]
        inventory_sheet.update_cell(found_row, QUANTITY_COLUMN_INDEX, new_quantity)
        transaction(transaction_sheet, requested_item["item_name"], requested_item["rarity"], requested_item["quantity_handled"], requested_item["transaction_info"])
        return -1

def check_stock(inventory_sheet, item_name, rarity):
    found_row = find_row(inventory_sheet, item_name, rarity)
    if found_row == None:
        return 0
    return int(inventory_sheet.cell(found_row, QUANTITY_COLUMN_INDEX).value)