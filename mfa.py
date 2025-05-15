import pyotp
import qrcode
import io
from fastapi.responses import StreamingResponse
from firestore import set_totp_secret, get_totp_secret

def generate_totp_qr(uid, email):
    totp = pyotp.TOTP(pyotp.random_base32())
    secret = totp.secret
    uri = totp.provisioning_uri(name=email, issuer_name="SecureScanner")

    set_totp_secret(uid, secret)

    img = qrcode.make(uri)
    buf = io.BytesIO()
    img.save(buf)
    buf.seek(0)
    return StreamingResponse(buf, media_type="image/png")

def verify_totp(uid, code):
    secret = get_totp_secret(uid)
    if not secret:
        return False
    totp = pyotp.TOTP(secret)
    return totp.verify(code)
