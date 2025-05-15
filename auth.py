import firebase_app  # Isso já inicializa o Firebase
from firebase_admin import auth

def verify_token(id_token: str):
    try:
        decoded_token = auth.verify_id_token(id_token)
        return decoded_token
    except Exception as e:
        return None


