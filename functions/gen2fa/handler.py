import json, base64, io, pyotp, qrcode
from common.db import get_conn

def handle(event, context):
    body = json.loads(event.body or "{}")
    username = body.get("username")
    if not username:
        return {"statusCode":400,"body":"username missing"}

    # 1. secret + URI
    secret = pyotp.random_base32()          # :contentReference[oaicite:2]{index=2}
    uri     = pyotp.totp.TOTP(secret).provisioning_uri(name=username,
                                                      issuer_name="COFRAP-ID")
    # 2. QR
    buf = io.BytesIO(); qrcode.make(uri).save(buf, format='PNG')
    uri_qr_b64 = base64.b64encode(buf.getvalue()).decode()

    # 3. stocker DB
    with get_conn() as c:
        with c.cursor() as cur:
            cur.execute("""
              UPDATE users SET mfa_secret=%s, gendate=NOW(), expired=false
              WHERE username=%s;
            """, (secret, username))

    return {"statusCode":200,
            "body":json.dumps({"secret":secret,"secret_qr":uri_qr_b64})}
