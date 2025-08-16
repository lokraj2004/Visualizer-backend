from flask import request, jsonify
from mongodb import store_command_in_firestore


def slider_value():
    data = request.get_json()
    value = data.get("value")
    store_command_in_firestore(value, collection_name="commands")
    print(f"Received slider value: {value}")
    return jsonify({"status": "success", "received": value})

