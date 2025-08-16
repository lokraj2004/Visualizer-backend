from datetime import datetime
from collections import defaultdict
from mongodb import get_collection

def sum_sensor_values(data_points):
    """Scalable summing logic — easily extendable in future."""
    return sum(dp['value'] for dp in data_points)

def get_usage_stats(sensor_ids, view_type):
    collection = get_collection()
    sensor_ids = [int(sid.strip()) for sid in sensor_ids.split(',') if sid.strip().isdigit()]
    print(sensor_ids)
    if view_type not in ['daywise', 'monthly', 'yearly']:
        return {"error": "Invalid view type"}, 400

    cursor = collection.find({
        "metadata.sensorId": {"$in": sensor_ids}
    })

    grouped_data = defaultdict(list)

    for doc in cursor:
        ts = doc['timestamp']
        if view_type == "daywise":
            key = ts.strftime("%Y-%m-%d")  # e.g., 2025-08-08
        elif view_type == "monthly":
            key = ts.strftime("%Y-%m")      # e.g., 2025-08
        else:
            key = ts.strftime("%Y")         # e.g., 2025

        grouped_data[key].append(doc)

    result = []
    for period, data_points in grouped_data.items():
        total = sum_sensor_values(data_points)
        result.append({"period": period, "total": round(total, 2)})
    print(result)
    # Sort chronologically
    result.sort(key=lambda x: x["period"])
    return result
