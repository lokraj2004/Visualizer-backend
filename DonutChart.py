
from collections import defaultdict
from mongodb import get_collection

def get_sensor_usage_counts(sensor_ids):
    collection = get_collection()

    # Convert sensor ID strings to integers
    sensor_ids = [int(sid.strip()) for sid in sensor_ids.split(",") if sid.strip().isdigit()]

    if not sensor_ids:
        return None, "Invalid or empty sensor IDs."

    pipeline = [
        {"$match": {"metadata.sensorId": {"$in": sensor_ids}}},
        {"$group": {
            "_id": "$metadata.sensorId",
            "count": {"$sum": 1}
        }}
    ]

    result = list(collection.aggregate(pipeline))

    if not result:
        return None, "No data found for provided sensor IDs."

    total = sum(item["count"] for item in result)

    usage = []
    for item in result:
        percent = round((item["count"] / total) * 100, 2)
        usage.append({
            "sensorId": item["_id"],
            "count": item["count"],
            "percentage": percent
        })

    return usage, None
