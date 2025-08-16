from SocketInstance import socketio
import time
import threading
from mongodb import get_collection

collection = get_collection()

def get_latest_sensor_data(sensor_id):
    document = collection.find_one(
        {"metadata.sensorId": int(sensor_id)},
        sort=[("timestamp", -1)]
    )
    if document:
        document["_id"] = str(document["_id"])
        document["timestamp"] = document["timestamp"].isoformat()
        return {
            "sensorId": document["metadata"]["sensorId"],
            "name": document["metadata"]["name"],
            "unit": document["metadata"]["unit"],
            "value": document["value"],
            "timestamp": document["timestamp"],
            "_id": document["_id"]
        }
    return None

def emit_latest_data_on_connect(initial_sensor_id="1"):
    current_sensor = {"id": int(initial_sensor_id)}  # Shared mutable object

    @socketio.on('connect')
    def handle_connect():
        print("Client connected — starting sensor emit thread")

        def emit_loop():
            while True:
                sensor_id = current_sensor["id"]  # Read current ID every time
                data = get_latest_sensor_data(sensor_id)
                print(f"[Emit] sensor_{sensor_id} →", data)
                if data:
                    socketio.emit(f"sensor_{sensor_id}", data)
                time.sleep(5)

        thread = threading.Thread(target=emit_loop, daemon=True)
        thread.start()

    @socketio.on("update_sensor_id")
    def handle_sensor_id_change(data):
        try:
            new_id = int(data.get("sensorId"))
            print(f"Updating sensor ID to: {new_id}")
            current_sensor["id"] = new_id
        except Exception as e:
            print("Invalid sensor ID update:", e)
