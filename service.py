import os
from flask_cors import CORS
from transformers import T5Tokenizer, T5ForConditionalGeneration
from flask import Flask, json, render_template, request, jsonify
import gspread
from google.oauth2.service_account import Credentials
import torch


# Training data file
TRAIN_DATA_FILE = "train_data.json"

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load the model
tokenizer = T5Tokenizer.from_pretrained("./robot_instruction_model")
model = T5ForConditionalGeneration.from_pretrained("./robot_instruction_model")

@app.route('/')
def index():
    return render_template('index.html')  # Ensure 'index.html' is in a 'templates' folder

@app.route("/welcome", methods=["GET"])
def welcome_command():    
    result = "How can I assist you today ?"
    return jsonify( {"response": result})

@app.route("/request", methods=["POST"])
def get_command():
    cmd_request = request.json.get('message')    
    print("request: ", cmd_request)
    result = generate_response(cmd_request)
    print("Generated command: ", result)
    return jsonify( {"response": result})


@app.route("/api/train", methods=["POST"])
def train_command():
    try:
        data = request.get_json()

       
        # Validate required fields
        required_fields = ["command", "method", "currentVolume", "finalVolume"]
        for field in required_fields:
            if field not in data or data[field] == "":
                return jsonify({"error": f"Missing or empty field: {field}"}), 400
            
        formatted_data = []

        #for entry in collected_data:
        # Extract command and parameters
        command = data["command"].strip()
        method = data["method"].strip()
        mwco = data["mwco"]
        current_volume = data["currentVolume"]
        current_buffer_volume = data["currentBufferVolume"]
        initial_concentrate = data["initialConcentrate"]
        final_concentrate = data["finalConcentrate"]
        final_volume = data["finalVolume"]
        start_exchange = data["startExchange"]
        step_size = data["stepSize"]
        exchange_volume = data["exchangeVolume"]

        # Convert structured JSON output to string format
        if command == "Concentrate":
            structured_json = {
                "text": command,
                "robot_command": {
                    "method": method,
                    "mwco": mwco,
                    "currentVolume": current_volume,
                    "initialConcentrate": initial_concentrate,
                    "finalVolume": final_volume,
                    "finalConcentrate": final_concentrate
                }
            }
        else:
            structured_json = {
                "text": command,
                "robot_command": {
                    "method": method,
                    "mwco": mwco,
                    "currentVolume": current_volume,
                    "currentBufferVolume": current_buffer_volume,
                    "initialConcentrate": initial_concentrate,
                    "finalConcentrate": final_concentrate,
                    "finalVolume": final_volume,
                    "startExchange": start_exchange,
                    "stepSize": step_size,
                    "exchangeVolume": exchange_volume
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
        return jsonify({"response": "Data saved successfully"}) 
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def generate_response(request):
    # Tokenize and generate
    input_ids = tokenizer.encode(request, return_tensors="pt")
    #outputs = model.generate(input_ids, max_length=150)
    outputs = model.generate(input_ids, max_length=128, num_beams=4, early_stopping=True)
    generated_commands = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return generated_commands
    
def save_training_data(data):
    if os.path.exists(TRAIN_DATA_FILE):
        with open(TRAIN_DATA_FILE, "r") as file:
            try:
                train_data = json.load(file)
            except json.JSONDecodeError:
                train_data = []
    else:
        train_data = []

    train_data.append(data)
    with open(TRAIN_DATA_FILE, "w") as file:
        json.dump(train_data, file, indent=4)

def save_training_data_to_gsheet(data):
    # Define the scope
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

    url ="https://docs.google.com/spreadsheets/d/1nrCTqupKIrwugKIuJt16GwA7CUPzndOH3T2XThv9tw0/edit?usp=sharing"

    # Add your service account credentials file
    creds = Credentials.from_service_account_file('./credential.json', scopes=scope)

    # Authorize the client
    client = gspread.authorize(creds)

    # Open the Google Sheet by url
    sheet = client.open_by_url(url).get_worksheet(0)
    for d in data:
        print("Input: ", d["input"])
        print("Output: ", d["output"])
        sheet.append_row([d["input"], d["output"]])  # Add a new row to the sheet
    


if __name__ == "__main__":
    app.run(  port=5000)