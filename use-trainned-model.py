from transformers import T5Tokenizer, T5ForConditionalGeneration
from flask import Flask, request, jsonify

app = Flask(__name__)

# Load the model
tokenizer = T5Tokenizer.from_pretrained("./robot_instruction_model")
model = T5ForConditionalGeneration.from_pretrained("./robot_instruction_model")


@app.route("/get-command", methods=["POST"])
def get_command():
    data = request.json
    cmd_request = data.get("request")
    print("request: ", cmd_request)
    result = generate_command(cmd_request)
    print("Generated command: ", result)
    return generate_command(result)

def generate_command(request):
    # Tokenize and generate
    input_ids = tokenizer.encode(request, return_tensors="pt")
    #outputs = model.generate(input_ids, max_length=150)
    outputs = model.generate(input_ids, max_length=128, num_beams=4, early_stopping=True)
    generated_commands = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return generated_commands
    

# request = ""
# while True:
#     print("Tell me what can I help you ? <Enter Q/q to quit")
#     request = input()
#     if request == "Q" or request == "q":
#         break
#     print("Request:", request)
#     print("Generated Command:", generate_command(request))


if __name__ == "__main__":
    app.run(host="localhost", port=5000)