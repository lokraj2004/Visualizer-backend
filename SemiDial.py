from flask import request, jsonify
from mongodb import get_collection

collection = get_collection()
def semi_dial():
    data = request.get_json()
    sensor_ids = data.get("sensorIds", [])
    threshold = 100  # assumed threshold

    total = 0
    count = 0

    for sid in sensor_ids:
        result = collection.find({"metadata.sensorId": sid})
        for r in result:
            total += r.get("value", 0)
            count += 1

    maintenance_score = round(total / count, 2) if count else 0

    return jsonify({
        "maintenanceScore": maintenance_score,
        "threshold": threshold
    })
