from fastapi import FastAPI, Request, HTTPException, status
from fastapi.responses import StreamingResponse, Response
from fastapi.middleware.cors import CORSMiddleware
from firebase_admin import auth
from mfa import generate_totp_qr, verify_totp
from firestore import get_totp_secret, set_totp_secret
from firebase_app import firebase_app  # inicializa Firebase Admin

app = FastAPI()

# Middleware CORS liberando todas as origens (sem allow_credentials)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5500",
        "http://127.0.0.1:5500",
        "https://seusite.com"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_user_id_from_token(request: Request) -> str:
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token ausente ou inválido")
    id_token = auth_header.split(" ")[1]
    try:
        decoded_token = auth.verify_id_token(id_token)
        return decoded_token["uid"]
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido ou expirado")

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


