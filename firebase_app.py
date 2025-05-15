# firebase_app.py
import json
import os
import base64
import firebase_admin
from firebase_admin import credentials

if not firebase_admin._apps:
   
    decoded_json = base64.b64decode(os.environ["GOOGLE_CREDENTIALS_B64"]).decode()
    cred = credentials.Certificate(json.loads(cred_json))
    firebase_admin.initialize_app(cred)
