# firebase_app.py
import json
import os
import firebase_admin
from firebase_admin import credentials

if not firebase_admin._apps:
    cred_json = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS_JSON")
    cred = credentials.Certificate(json.loads(cred_json))
    firebase_admin.initialize_app(cred)
