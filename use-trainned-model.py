import os
from flask_cors import CORS
from transformers import T5Tokenizer, T5ForConditionalGeneration
from flask import Flask, json, render_template, request, jsonify


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

def convert_data(input_file, output_file):
    try:
        # Load collected training data
        with open(input_file, "r") as f:
            collected_data = json.load(f)

        formatted_data = []

        for entry in collected_data:
            # Extract input command and expected structured JSON output
            command = entry.get("command", "").strip()
            structured_json = entry.get("ai_generated_json", {})

            if command and structured_json:
                formatted_entry = {
                    "input": f"translate command: {command}",
                    "target": json.dumps(structured_json)  # Convert JSON to string
                }
                formatted_data.append(formatted_entry)

        # Save formatted data
        with open(output_file, "w") as f:
            json.dump(formatted_data, f, indent=4)

        print(f"✅ Successfully converted data! Saved as {output_file}")

    except Exception as e:
        print(f"❌ Error processing data: {e}")
        return False

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
        current_volume = data["currentVolume"]
        initial_concentrate = data["initialConcentrate"]
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
                    "currentVolume": current_volume,
                    "initialConcentrate": initial_concentrate,
                    "finalVolume": final_volume,
                }
            }
        else:
            structured_json = {
                "text": command,
                "robot_command": {
                    "method": method,
                    "currentVolume": current_volume,
                    "initialConcentrate": initial_concentrate,
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
        save_training_data(formatted_data)
        return jsonify({"response": "Data saved successfully"}) 
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(  port=5000)