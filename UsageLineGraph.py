# linegraph_api.py
from flask import jsonify, request
from bson.son import SON
from mongodb import get_collection
from datetime import datetime
from collections import defaultdict

def get_linegraph_data():
    sensor_ids_str = request.args.get("sensorIds")
    mode = request.args.get("mode", "daywise")

    if not sensor_ids_str:
        return jsonify({"error": "Sensor IDs required"}), 400

    try:
        sensor_ids = [int(sid.strip()) for sid in sensor_ids_str.split(",")]
    except ValueError:
        return jsonify({"error": "Invalid sensor IDs"}), 400

    try:
        result = sum_sensor_values_by_timestamp(sensor_ids, mode)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def sum_sensor_values_by_timestamp(sensor_ids, mode='daywise'):
    pipeline = [
        {"$match": {"metadata.sensorId": {"$in": sensor_ids}}},
        {"$project": {
            "sensorId": "$metadata.sensorId",
            "value": 1,
            "timestamp": {
                "$dateToString": {
                    "format": {
                        "daywise": "%Y-%m-%d",
                        "monthly": "%Y-%m",
                        "yearly": "%Y"
                    }[mode],
                    "date": "$timestamp"
                }
            }
        }},
        {"$group": {
            "_id": {"timestamp": "$timestamp", "sensorId": "$sensorId"},
            "total": {"$sum": "$value"}
        }},
        {"$sort": SON([("_id.timestamp", 1)])}
    ]
    collection = get_collection()
    results = collection.aggregate(pipeline)
    grouped = defaultdict(dict)
    print (grouped)
    for doc in results:
        date = doc["_id"]["timestamp"]
        sensor_id = doc["_id"]["sensorId"]
        grouped[date][sensor_id] = doc["total"]

    return grouped
