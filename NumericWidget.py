# numeric_handler.py
from mongodb import store_command_in_firestore


def handle_numeric(request):
    if request.method == "POST":
        data = request.get_json()
        value = data.get("value")
        store_command_in_firestore(value,collection_name="commands")
        print(f"Numeric value received: {value}")
        return {"message": f"Received value {value}"}
    return {"message": "Send a POST request with 'value' field"}
