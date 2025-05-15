from fastapi import FastAPI, Request, HTTPException, status
from fastapi.responses import StreamingResponse, Response
from firebase_admin import auth
from mfa import generate_totp_qr, verify_totp
from firestore import get_totp_secret, set_totp_secret
from firebase_app import firebase_app  # inicializa Firebase Admin

app = FastAPI()

@app.middleware("http")
async def add_cors_headers(request: Request, call_next):
    print(f"[CORS Middleware] Método: {request.method} | Origin: {request.headers.get('origin')}")
    if request.method == "OPTIONS":
        headers = {
            "Access-Control-Allow-Origin": request.headers.get("origin", "*"),
            "Access-Control-Allow-Methods": "GET,POST,PUT,DELETE,OPTIONS",
            "Access-Control-Allow-Headers": request.headers.get("access-control-request-headers", "*"),
            "Access-Control-Allow-Credentials": "true",
        }
        print("[CORS Middleware] Respondendo OPTIONS com headers:", headers)
        return Response(status_code=200, headers=headers)

    response = await call_next(request)
    response.headers.setdefault("Access-Control-Allow-Origin", request.headers.get("origin", "*"))
    response.headers.setdefault("Access-Control-Allow-Methods", "GET,POST,PUT,DELETE,OPTIONS")
    response.headers.setdefault("Access-Control-Allow-Headers", request.headers.get("access-control-request-headers", "*"))
    response.headers.setdefault("Access-Control-Allow-Credentials", "true")
    print(f"[CORS Middleware] Adicionando headers CORS na resposta para método {request.method}")
    return response

def get_user_id_from_token(request: Request) -> str:
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token ausente ou inválido")
    id_token = auth_header.split(" ")[1]
    try:
        decoded_token = auth.verify_id_token(id_token)
        return decoded_token["uid"]
    except Exception as e:
        print(f"[Auth] Erro ao verificar token: {e}")
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

