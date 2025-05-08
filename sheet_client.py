import gspread
from google.oauth2.service_account import Credentials

def get_sheet(sheet_name="Inventory"):
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]
    creds = Credentials.from_service_account_file("credentials.json", scopes=scope)
    client = gspread.authorize(creds)
    return client.open(sheet_name)
