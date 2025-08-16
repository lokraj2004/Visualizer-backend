from pymongo import MongoClient
from FirebaseSetup import db_firestore
from datetime import datetime


# Singleton pattern (reuse connection)
_client = None

def get_db():
    global _client
    if _client is None:
        _client = MongoClient("mongodb://localhost:27017/")
    return _client["SensorReadings"]  # Your MongoDB database name

def get_collection():
    db = get_db()
    return db["SensorData"]  # Your time-series collection name

def store_command_in_firestore(command, collection_name="commands"):

    if not command:
        raise ValueError("Command cannot be empty")

    db_firestore.collection(collection_name).add({
        "command": command,
        "timestamp": datetime.utcnow()
    })
