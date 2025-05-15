# firebase_app.py
import json
import os
import base64
import firebase_admin
from firebase_admin import credentials

if not firebase_admin._apps:
    # Decodifica a variável de ambiente contendo o JSON base64
    decoded_json = base64.b64decode(os.environ["GOOGLE_CREDENTIALS_B64"]).decode()
    cred = credentials.Certificate(json.loads(decoded_json))
    firebase_app = firebase_admin.initialize_app(cred)
else:
    firebase_app = firebase_admin.get_app()
