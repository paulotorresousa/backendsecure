from fastapi import FastAPI, Header, HTTPException, Form
from mfa import generate_totp_qr, verify_totp
from firestore import get_totp_secret
from auth import verify_token

app = FastAPI()

@app.get("/setup-mfa")
def setup_mfa(authorization: str = Header(...)):
    user = verify_token(authorization)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")
    return generate_totp_qr(user["uid"], user["email"])

@app.post("/verify-totp")
def verify(code: str = Form(...), authorization: str = Header(...)):
    user = verify_token(authorization)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")
    valid = verify_totp(user["uid"], code)
    if not valid:
        raise HTTPException(status_code=400, detail="Invalid code")
    return {"success": True}

@app.get("/check-mfa-status")
def check_mfa(authorization: str = Header(...)):
    user = verify_token(authorization)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")
    secret = get_totp_secret(user["uid"])
    return {"mfa_enabled": bool(secret)}
