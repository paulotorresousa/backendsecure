import json
import os
import firebase_admin
from firebase_admin import credentials

# Pega o JSON direto da variável de ambiente
firebase_json = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS_JSON")

# Converte a string para dicionário
cred = credentials.Certificate(json.loads(firebase_json))

# Inicializa o Firebase Admin
firebase_admin.initialize_app(cred)

