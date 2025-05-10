from sheet_client import get_sheet
import inventory
import helper



def main():
    helper.clear_screen()
    sheet = get_sheet("Inventory")
    inventory_sheet = sheet.worksheet("Inventory")
    transaction_sheet = sheet.worksheet("Transactions")
    running = True

    print("Inventory Manager")
    print("-----------------\n")

    username = helper.get_user_info()

    while running == True:
        action = input("Enter command, \"info\" for list of commands: ").strip().lower()

        #add item, remove item, info, quit
        match action:
            case "add item" | "add" | "deposit":
                helper.process_inventory_transaction(username, inventory_sheet, transaction_sheet, transaction_type="deposit")

            case "remove item" | "remove" | "withdraw":
                helper.process_inventory_transaction(username, inventory_sheet, transaction_sheet, transaction_type="withdraw")
                        
            case "info" | "help":
                helper.print_help_text()
                
            case "check stock" | "lookup" | "stock":
                item, rarity = helper.get_item_info(quantity_needed=False)
                result = inventory.check_stock(inventory_sheet, item, rarity)
                print(f"Item {item} with quality {rarity} has {result} in stock.")

            case "edit settings" | "settings":
                helper.update_settings()

            case "batch":
                while True:
                    add_or_remove = input("Batch deposit or batch withdraw?: ")
                    if add_or_remove in ["deposit", "withdraw", "add", "remove"]:
                        break
                    else:
                        print("Please enter \"deposit\", \"add\", \"withdraw\" or \"remove\"")
                    
                if add_or_remove in ["add", "deposit"]:
                    while True:
                        helper.process_inventory_transaction(username, inventory_sheet, transaction_sheet, transaction_type="deposit")
                        if input("Continue? ") not in ["yes", "y"]:
                            break
                else:
                    while True:
                        helper.process_inventory_transaction(username, inventory_sheet, transaction_sheet, transaction_type="withraw")
                        if input("Continue? ") in ["yes", "y"]:
                            break

            case "quit" | "exit":
                running = False
                print("exiting...")

            case _:
                print("Invalid input, please see \"info\" for commands.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting...")
