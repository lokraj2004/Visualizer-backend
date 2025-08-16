from SocketInstance import socketio
from mongodb import get_collection
import threading
import time

collection = get_collection()

def get_latest_n_data(sensor_ids, limit=20):
    results = []
    for sid in sensor_ids:
        cursor = collection.find(
            {"metadata.sensorId": int(sid)},
            sort=[("timestamp", -1)],
            limit=limit
        )
        for doc in cursor:
            results.append({
                "sensorId": doc["metadata"]["sensorId"],
                "name": doc["metadata"]["name"],
                "value": doc["value"],
                "timestamp": doc["timestamp"].isoformat()
            })
    return results

# Shared mutable state to allow updates without restarting thread
current_sensors = {"ids": []}

@socketio.on('line_graph_subscribe')
def handle_line_graph_subscription(data):
    sensor_ids_raw = data.get("sensorIds", "")
    if not sensor_ids_raw:
        return

    try:
        sensor_ids = [int(sid.strip()) for sid in sensor_ids_raw.split(",") if sid.strip().isdigit()]
        print(f"[LineGraphSocket] Subscribed to: {sensor_ids}")
        current_sensors["ids"] = sensor_ids
    except Exception as e:
        print("Invalid sensor ID list:", e)
        return

    def emit_loop():
        while True:
            sensor_ids = current_sensors["ids"]  # Read latest sensor IDs dynamically
            graph_data = get_latest_n_data(sensor_ids)
            socketio.emit("line_graph_data", graph_data)
            time.sleep(5)

    thread = threading.Thread(target=emit_loop, daemon=True)
    thread.start()

@socketio.on("update_linegraph_sensor_ids")
def handle_linegraph_sensor_update(data):
    try:
        new_ids_raw = data.get("sensorIds", "")
        new_ids = [int(sid.strip()) for sid in new_ids_raw.split(",") if sid.strip().isdigit()]
        print(f"Updating line graph sensor IDs to: {new_ids}")
        current_sensors["ids"] = new_ids
    except Exception as e:
        print("Invalid sensor ID update for line graph:", e)
