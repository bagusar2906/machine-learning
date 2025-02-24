import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
import json
from pydantic import BaseModel, field_validator, validator
from typing import Optional
import gspread
from google.oauth2.service_account import Credentials
from dotenv import load_dotenv

app = FastAPI()


class Data(BaseModel):
    command: str
    method: str
    mwco: int
    currentVolume: float   
    currentBufferVolume: Optional[float] = None
    initialConcentrate: Optional[float] = None
    finalConcentrate: Optional[float] = None
    finalVolume: Optional [float] = None
    startExchange: Optional[float] = None
    stepSize: Optional[float] = None
    exchangeVolume: Optional[float] = None
    
    @field_validator("currentVolume")
    def currentVolume_must_be_positive(cls, value):       
        if value < 0:
            raise ValueError("Current volume must be a positive number")
        return value
    
    @field_validator("finalVolume")
    def finalVolume_must_be_positive(cls, value):       
        if value < 0:
            raise ValueError("Final volume must be a positive number")
        return value
    
    
@app.post("/api/train")
def train_command(request: Data):
    try:
       
        # Validate required fields
        required_fields = ["command", "method", "currentVolume", "finalVolume"]
        for name, value in request:
            if value == "" and name in required_fields:
                return JSONResponse(content={"error": f"Missing or empty field: {name}"}, status_code=400)
          
        formatted_data = []

        #for entry in collected_data:
        # Extract command and parameters
        command = request.command.strip()

        # Convert structured JSON output to string format
        if command == "Concentrate":
            structured_json = {
                "text": command,
                "robot_command": {
                    "method": request.method,
                    "mwco": request.mwco,
                    "currentVolume": request.currentVolume,
                    "initialConcentrate": request.initialConcentrate,
                    "finalVolume": request.finalVolume,
                    "finalConcentrate": request.finalConcentrate
                }
            }
        else:
            structured_json = {
                "text": command,
                "robot_command": {
                    "method": request.method,
                    "mwco": request.mwco,
                    "currentVolume": request.currentVolume,
                    "currentBufferVolume": request.currentBufferVolume,
                    "initialConcentrate": request.initialConcentrate,
                    "finalConcentrate": request.finalConcentrate,
                    "finalVolume": request.finalVolume,
                    "startExchange": request.startExchange,
                    "stepSize": request.stepSize,
                    "exchangeVolume": request.exchangeVolume
                }
            }

        # Format data for T5 training
        formatted_entry = {
            "input": f"{command}",
            "output": json.dumps(structured_json.get("robot_command",{}))  # Convert JSON to string
        }
        formatted_data.append(formatted_entry)

        # Save formatted data
        save_training_data_to_gsheet(formatted_data)
        return JSONResponse(content={"response": "Data saved successfully"})
    
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

    
# Serve static files from the "build" directory
app.mount("/", StaticFiles(directory="clientapp/build", html=True), name="static")

def load_credentials_from_file():
    # Define the scope
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

    # Add your service account credentials file
    creds = Credentials.from_service_account_file('../credential.json', scopes=scope)

    # Authorize the client
    client = gspread.authorize(creds)
    return client

def load_credentials_from_env():
# Step 1: Ensure the JSON credentials are stored in an environment variable
# For example, set the environment variable in your terminal:
# export GOOGLE_CREDENTIALS='{"type": "service_account", "project_id": "your-project-id", ...}'
# Note: It might not work in Windows due MAX_LENGTH limitation
# Step 2: Load the JSON credentials from the environment variable
    load_dotenv()
    google_credentials_json = os.getenv('GOOGLE_CREDENTIALS')

    if not google_credentials_json:
        raise ValueError("GOOGLE_CREDENTIALS environment variable is not set.")

    # Parse the JSON string into a dictionary
    credentials_info = json.loads(google_credentials_json)

    # Step 3: Create credentials using the service_account.Credentials class
    credentials = Credentials.from_service_account_info(credentials_info)

    # Now you can use `credentials` to authenticate with Google services
    print("Credentials loaded successfully!")
    print("Project ID:", credentials_info['project_id'])
     # Authorize the client
    client = gspread.authorize(credentials)
    return client


def save_training_data_to_gsheet(data):
  
    url ="https://docs.google.com/spreadsheets/d/1nrCTqupKIrwugKIuJt16GwA7CUPzndOH3T2XThv9tw0/edit?usp=sharing"


    # Authorize the client
    client = load_credentials_from_file()

    # Open the Google Sheet by url
    sheet = client.open_by_url(url).get_worksheet(0)
    for d in data:
        print("Input: ", d["input"])
        print("Output: ", d["output"])
        sheet.append_row([d["input"], d["output"]])  # Add a new row to the sheet
  

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)