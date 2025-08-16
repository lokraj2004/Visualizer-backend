from flask import request, jsonify
from mongodb import store_command_in_firestore
toggle_state = {"is_on": False}

def handle_toggle(request):
    global toggle_state

    if request.method == "POST":
        data = request.get_json()
        if data.get("state") == "on":
            toggle_state["is_on"] = True
            print("Toggle ON")
            command = "leds on"
            store_command_in_firestore(command, collection_name="commands")
            return {"message": "Toggle turned ON", "state": toggle_state["is_on"]}
        else:
            toggle_state["is_on"] = False
            print("Toggle OFF")
            command = "leds off"
            store_command_in_firestore(command, collection_name="commands")
            return {"message": "Toggle turned OFF", "state": toggle_state["is_on"]}

    # For GET request
    return {"state": toggle_state["is_on"]}