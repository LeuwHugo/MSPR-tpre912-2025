import json, os
from datetime import datetime, timedelta
from passlib.hash import bcrypt
import pyotp
from common.db import get_conn

EXPIRY = timedelta(days=183)   # ~6 months

def handle(event, context):
    data = json.loads(event.body or "{}")
    user, pwd, code = data.get("username"), data.get("password"), data.get("totp")
    if not all([user, pwd, code]):
        return {"statusCode":400,"body":"missing fields"}

    with get_conn() as c:
        with c.cursor() as cur:
            cur.execute("SELECT password_hash,mfa_secret,gendate,expired FROM users WHERE username=%s;",
                        (user,))
            row = cur.fetchone()
    if not row:
        return {"statusCode":401,"body":"invalid creds"}

    pwd_hash, mfa, gendate, expired = row
    if expired or (datetime.utcnow() - gendate) > EXPIRY:
        return {"statusCode":403,"body":"expired"}

    if not bcrypt.verify(pwd, pwd_hash) or \
       not pyotp.TOTP(mfa).verify(code, valid_window=1):
        return {"statusCode":401,"body":"invalid creds"}

    return {"statusCode":200,"body":"OK"}
