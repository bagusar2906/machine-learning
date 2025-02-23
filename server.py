from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse

import json
from pydantic import BaseModel, validator
from typing import Optional

app = FastAPI()


# Example REST API endpoint
@app.get("/api/hello")
def hello():
    return {"message": "Hello from FastAPI!"}

class UserWithValidation(BaseModel):
    name: str
    age: int
    email: str

    @validator("age")
    def age_must_be_positive(cls, value):
        if value < 0:
            raise ValueError("Age must be a positive number")
        return value

@app.post("/users-with-validation/")
def create_user_with_validation(user: UserWithValidation):
    return {"message": "User created", "user": user}

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
        return JSONResponse(content={"response": "Data saved successfully"})
    
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

    
# Serve static files from the "build" directory
app.mount("/", StaticFiles(directory="clientapp/build", html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)