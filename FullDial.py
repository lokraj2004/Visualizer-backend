from flask import request, jsonify
from mongodb import get_collection
from bson.json_util import dumps

THRESHOLD = 1000  # Arbitrary threshold
collection = get_collection()
def get_full_dial_data():
    try:
        data = request.json
        sensor_id = int(data.get("sensorId"))
        print(sensor_id)
        total_usage = 0
        cursor = collection.find({"metadata.sensorId": sensor_id})
        for doc in cursor:
            total_usage += float(doc.get("value", 0))

        return jsonify({
            "sensorId": sensor_id,
            "totalUsage": total_usage,
            "threshold": THRESHOLD
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 400
