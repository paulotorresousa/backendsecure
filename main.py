from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from firebase_admin import auth
from mfa import generate_totp_qr, verify_totp
from firestore import get_totp_secret, set_totp_secret
import firebase_app  # inicialização do Firebase Admin
from utils import get_user_id_from_token  # você já deve ter criado essa função

app = FastAPI()

# 🛡️ Habilita CORS para qualquer origem (durante desenvolvimento)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, substitua por seu domínio (ex: ["https://seusite.com"])
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"msg": "SecureScanner backend online."}

@app.get("/check-mfa-status")
def check_mfa_status(request: Request):
    user_id = get_user_id_from_token(request)
    secret = get_totp_secret(user_id)
    return {"mfa_enabled": secret is not None}

@app.get("/setup-mfa")
def setup_mfa(request: Request):
    user_id = get_user_id_from_token(request)
    secret, img_bytes = generate_totp_qr(user_id)
    set_totp_secret(user_id, secret)
    return StreamingResponse(img_bytes, media_type="image/png")

@app.post("/verify-totp")
def verify_totp_route(request: Request, code: str = ""):
    user_id = get_user_id_from_token(request)
    secret = get_totp_secret(user_id)
    if not secret:
        raise HTTPException(status_code=400, detail="MFA não configurado")
    if not verify_totp(secret, code):
        raise HTTPException(status_code=401, detail="Código inválido")
    return {"msg": "MFA verificado com sucesso"}
