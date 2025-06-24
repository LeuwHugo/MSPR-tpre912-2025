import json, os, secrets, string, base64, io, qrcode
from passlib.hash import bcrypt
from datetime import datetime
from common.db import get_conn

ALPHA = string.ascii_letters + string.digits + string.punctuation

def handle(event, context):
    body = json.loads(event.body or "{}")
    username = body.get("username")
    if not username:
        return {"statusCode":400,"body":"username missing"}

    # 1. générer mot de passe 24 car.
    pwd_plain = ''.join(secrets.choice(ALPHA) for _ in range(24))
    pwd_hash  = bcrypt.using(rounds=12).hash(pwd_plain)

    # 2. QR code PNG en Base64
    img_buf = io.BytesIO()
    qrcode.make(pwd_plain).save(img_buf, format='PNG')
    pwd_qr_b64 = base64.b64encode(img_buf.getvalue()).decode()

    # 3. Insert DB
    with get_conn() as c:
        with c.cursor() as cur:
            cur.execute("""
              INSERT INTO users(username,password_hash, mfa_secret)
              VALUES (%s,%s,'') ON CONFLICT(username) DO UPDATE
              SET password_hash=EXCLUDED.password_hash,
                  gendate=NOW(), expired=false;
            """, (username, pwd_hash))

    return {
        "statusCode": 200,
        "body": json.dumps({"password": pwd_plain,
                            "password_qr": pwd_qr_b64})
    }
