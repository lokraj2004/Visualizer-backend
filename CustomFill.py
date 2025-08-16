# custom_fill_api.py
from flask import request, jsonify
from bson.son import SON
from mongodb import get_collection

def get_custom_fill_data():
    data = request.json
    sensor_ids_str = data.get("sensorIds", "")
    threshold = 1000  # You can modify this threshold

    try:
        sensor_ids = [int(sid.strip()) for sid in sensor_ids_str.split(",") if sid.strip()]
        if not sensor_ids:
            return jsonify({"error": "No valid sensor IDs provided"}), 400
    except Exception as e:
        return jsonify({"error": f"Invalid sensor ID format: {e}"}), 400

    try:
        pipeline = [
            {"$match": {"metadata.sensorId": {"$in": sensor_ids}}},
            {"$group": {"_id": None, "total": {"$sum": "$value"}}}
        ]
        result = list(get_collection().aggregate(pipeline))
        total_usage = result[0]["total"] if result else 0

        return jsonify({
            "success": True,
            "data": {
                "totalUsage": total_usage,
                "threshold": threshold,
                "status": "Overload" if total_usage >= threshold else "Normal"
            }
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
