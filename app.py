from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

DATA_DIR = "/var/lib/backend_data"
DATA_FILE = os.path.join(DATA_DIR, "messages.json")

def load_messages():
    os.makedirs(DATA_DIR, exist_ok=True)

    if not os.path.exists(DATA_FILE):
        return []

    with open(DATA_FILE, "r") as file:
        return json.load(file)

def save_messages(messages):
    os.makedirs(DATA_DIR, exist_ok=True)

    with open(DATA_FILE, "w") as file:
        json.dump(messages, file)

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "healthy"})

@app.route("/messages", methods=["GET"])
def get_messages():
    return jsonify(load_messages())

@app.route("/messages", methods=["POST"])
def add_message():
    data = request.get_json()
    messages = load_messages()

    messages.append(data["message"])
    save_messages(messages)

    return jsonify({"message": "Message added"})

@app.route("/messages", methods=["DELETE"])
def delete_message():
    messages = load_messages()
    index = request.args.get("index", type=int)

    if index is None or index < 0 or index >= len(messages):
        return jsonify({"error": "Invalid index"}), 400

    messages.pop(index)
    save_messages(messages)

    return jsonify({"message": "Message deleted"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)