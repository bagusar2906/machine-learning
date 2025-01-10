from transformers import T5Tokenizer, T5ForConditionalGeneration
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

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
    


if __name__ == "__main__":
    app.run(host="localhost", port=5000)