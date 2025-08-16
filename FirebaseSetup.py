# firebase_setup.py

import firebase_admin
from firebase_admin import credentials, firestore,db
import datetime

cred = credentials.Certificate("serviceAccountKey.json")

# Initialize app only once
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred, {
        'databaseURL': "https://coupling-together-5e78a-default-rtdb.firebaseio.com"
    })

db_firestore = firestore.client()
db_realtime = db

