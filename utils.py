import json
import os

FILE_PATH = "user_data.json"

LEVEL_CAPS = [100, 250, 500, 1000, 2000]

def load_data():
    if not os.path.exists(FILE_PATH):
        return {}
    with open(FILE_PATH, "r") as file:
        return json.load(file)

def save_data(data):
    with open(FILE_PATH, "w") as file:
        json.dump(data, file, indent=4)

def error_response(error_type: str):
    return {"status": "ERROR", "error_type": error_type}
