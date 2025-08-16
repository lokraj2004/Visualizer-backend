
from datetime import datetime, timedelta
from pymongo import DESCENDING
from mongodb import get_collection

def get_sensor_stats_by_id(sensor_id):
    col = get_collection()

    now = datetime.utcnow()
    past_24h = now - timedelta(hours=24)

    pipeline = [
        {
            "$match": {
                "metadata.sensorId": sensor_id,
                # "timestamp": {"$gte": past_24h}
            }
        },
        {
            "$group": {
                "_id": "$metadata.sensorId",
                "average": {"$avg": "$value"},
                "minimum": {"$min": "$value"},
                "maximum": {"$max": "$value"},
                "sum": {"$sum": "$value"},
                "unit": {"$first": "$metadata.unit"},
                "title": {"$first": "$metadata.name"}
            }
        }
    ]

    stats = list(col.aggregate(pipeline))
    latest = col.find_one(
        {"metadata.sensorId": sensor_id},
        sort=[("timestamp", DESCENDING)]
    )
    print(latest)
    if not stats or not latest:
        return None  # invalid sensor ID

    result = stats[0]
    return {
        "average": round(result["average"], 2),
        "minimum": result["minimum"],
        "maximum": result["maximum"],
        "sum": round(result["sum"], 2),
        "unit": result["unit"],
        "title": result["title"],
        "current": latest["value"],
        "timestamp": latest["timestamp"].isoformat()
    }
