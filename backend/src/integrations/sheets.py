import gspread 
from oauth2client.service_account import ServiceAccountCredentials
import os 
from dotenv import load_dotenv

load_dotenv()

class GoogleSheetsClient:
    def __init__(self):
        self.scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        self.creds_path = os.getenv('GOOGLE_SHEET_CREDENTIALS_PATH')
        self.spreadsheet_id = os.getenv('GOOGLE_SHEET_ID')
        
        if not self.creds_path:
            raise ValueError("GOOGLE_SHEET_CREDENTIALS_PATH environment variable is required but not set")
        if not self.spreadsheet_id:
            raise ValueError("GOOGLE_SHEET_ID environment variable is required but not set")

    def connect(self):
        try:
            creds = ServiceAccountCredentials.from_json_keyfile_name(self.creds_path, self.scope)
            client = gspread.authorize(creds)
            sheet = client.open_by_key(self.spreadsheet_id).sheet1
            return sheet
        except Exception as e:
            print(f"Error connecting to Google Sheets: {e}")
            return None
        
if __name__ == "__main__":
    test_client = GoogleSheetsClient()
    sheet = test_client.connect()
    if sheet:
        print("Successfully connected to Google Sheets!")
        # NOTE: Removed destructive insert_row call to prevent accidental data modification
        # To test insertion, use a dedicated test spreadsheet and set TEST_MODE=true
        print("Connection test completed successfully.")
    else:
        print("Failed to connect to Google Sheets.")