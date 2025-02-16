import gspread
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

# Define the scope
#scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

# Define the scope
scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

# Add your service account credentials file
creds = Credentials.from_service_account_file('../credential.json', scopes=scope)

# Authorize the client
client = gspread.authorize(creds)

# Initialize the Google Drive API
drive_service = build('drive', 'v3', credentials=creds)

# List all Google Spreadsheets in your Drive
response = drive_service.files().list(
    q="mimeType='application/vnd.google-apps.spreadsheet'",
    fields="files(id, name)"
).execute()

# Extract and print the spreadsheet names and IDs
spreadsheets = response.get('files', [])
for spreadsheet in spreadsheets:
    print(f"Name: {spreadsheet['name']}, ID: {spreadsheet['id']}")

# Open the Google Sheet by name
sheet = client.open("Training-Dataset")
#.get_worksheet(0)  # or use .get_worksheet(index) for a specific sheet

# Read all records
records = sheet.get_all_records()

# Print the records
for record in records:
    print(record)