# firebase_app.py
import json
import os
import base64
import firebase_admin
from firebase_admin import credentials

if not firebase_admin._apps:
    cred_json = os.environ.get("GOOGLE_CREDENTIALS_B64")
    decoded_json = base64.b64decode(encoded).decode()
    cred = credentials.Certificate(json.loads(cred_json))
    firebase_admin.initialize_app(cred)
