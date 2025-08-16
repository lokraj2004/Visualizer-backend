from mongodb import store_command_in_firestore


def handle_picklist_selection(data):
    selected_value = data.get("selected")
    store_command_in_firestore(selected_value,collection_name="commands")
    print(f"Picklist selection received: {selected_value}")
    return {"message": f"Selection '{selected_value}' received successfully"}