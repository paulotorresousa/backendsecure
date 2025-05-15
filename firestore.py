import firebase_app 
from firebase_admin import firestore

db = firestore.client()

def set_totp_secret(uid, secret):
    db.collection("users").document(uid).update({"totp_secret": secret})

def get_totp_secret(uid):
    doc = db.collection("users").document(uid).get()
    return doc.to_dict().get("totp_secret") if doc.exists else None
