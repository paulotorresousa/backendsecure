import firebase_app  # Garante a inicialização
from firebase_admin import firestore

db = firestore.client()

def set_totp_secret(uid, secret):
    # Usa set() com merge=True para criar ou atualizar com segurança
    db.collection("users").document(uid).set({"totp_secret": secret}, merge=True)

def get_totp_secret(uid):
    doc = db.collection("users").document(uid).get()
    if doc.exists:
        data = doc.to_dict()
        return data.get("totp_secret")
    return None

