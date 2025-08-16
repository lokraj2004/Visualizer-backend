from mongodb import store_command_in_firestore
from flask import Flask, jsonify, request

def submit_text():
    data = request.get_json()
    text = data.get("text")
    store_command_in_firestore(text, collection_name="commands")
    print(f"Received text: {text}")
    return jsonify({"status": "success", "received": text})