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
                item, rarity, quantity = helper.get_item_info(quantity_needed=True)
                transaction_info = helper.get_transaction_info(username=username, transaction_type="deposit")

                inventory.add_item(inventory_sheet, transaction_sheet, item, rarity, quantity, transaction_info)
                print(f"Added {item} with rarity: {rarity} and count: {quantity}.")

            case "remove item" | "remove" | "withdraw":
                item, rarity, quantity = helper.get_item_info(quantity_needed=True)
                transaction_info = helper.get_transaction_info(username=username, transaction_type="withdraw")

                result = inventory.remove_item(inventory_sheet, transaction_sheet, item, rarity, quantity, transaction_info)

                if result == -1:
                    print("Success")
                else:
                    print(f"Insufficent stock. {item} has {result} in stock.")
                        
            case "info" | "help":
                print("""Commands are:
                      \"add item\" or \"add\" or \"deposit\", 
                      \"remove item\" or \"remove\" or \"withdraw\", 
                      \"check stock\" or \"lookup\" or \"stock\",
                      \"edit settings\" or \"settings\", 
                      \"info\" or \"help\", 
                      \"quit\" or \"exit\"""")
                
            case "check stock" | "lookup" | "stock":
                item, rarity = helper.get_item_info(quantity_needed=False)
                result = inventory.check_stock(inventory_sheet, item, rarity)
                print(f"Item {item} with quality {rarity} has {result} in stock.")

            case "edit settings" | "settings":
                helper.update_settings()

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
