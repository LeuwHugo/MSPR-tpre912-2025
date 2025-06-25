from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import uuid, secrets, string, io, base64, qrcode, pyotp, datetime, os, psycopg2
from passlib.hash import bcrypt

app = FastAPI(docs_url="/")

# CORS pour le front Vite (http://localhost:5173)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def db():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "db"),
        port=5432,
        dbname="cofrap",
        user="faas",
        password="faaspass"
    )

ALPHA = string.ascii_letters + string.digits + string.punctuation

class User(BaseModel):
    username: str

class Login(User):
    password: str
    totp: str

class ResetRequest(BaseModel):
    username: str

class ResetPassword(BaseModel):
    token: str
    new_password: str

@app.post("/genpwd")
def genpwd(u: User):
    pwd = ''.join(secrets.choice(ALPHA) for _ in range(24))
    pwd_hash = bcrypt.hash(pwd)
    img = io.BytesIO()
    qrcode.make(pwd).save(img, 'PNG')

    with db() as conn, conn.cursor() as cur:
       cur.execute("""
           INSERT INTO users(username, password_hash, mfa_secret)
           VALUES (%s, %s, '')
           ON CONFLICT(username) DO UPDATE
             SET password_hash = EXCLUDED.password_hash,
                 gendate = NOW(),
                 expired = false;
       """, (u.username, pwd_hash))

    return {
        "password": pwd,
        "password_qr": base64.b64encode(img.getvalue()).decode()
    }

@app.post("/gen2fa")
def gen2fa(u: User):
    secret = pyotp.random_base32()
    uri = pyotp.totp.TOTP(secret).provisioning_uri(u.username, "COFRAP-ID")
    img = io.BytesIO()
    qrcode.make(uri).save(img, 'PNG')

    with db() as conn, conn.cursor() as cur:
        cur.execute("""
            UPDATE users
               SET mfa_secret = %s,
                   gendate = NOW(),
                   expired = false
             WHERE username = %s;
        """, (secret, u.username))

    return {
        "secret": secret,
        "secret_qr": base64.b64encode(img.getvalue()).decode()
    }

@app.post("/authuser")
def authuser(l: Login):
    with db() as conn, conn.cursor() as cur:
        cur.execute("""
            SELECT password_hash, mfa_secret, gendate, expired
              FROM users
             WHERE username = %s;
        """, (l.username,))
        row = cur.fetchone()

    if not row:
        raise HTTPException(status_code=401, detail="invalid credentials")

    pwd_hash, mfa, gendate, expired = row

    if expired or (datetime.datetime.utcnow() - gendate).days > 183:
        raise HTTPException(status_code=403, detail="credentials expired")

    if not bcrypt.verify(l.password, pwd_hash) or not pyotp.TOTP(mfa).verify(l.totp, valid_window=1):
        raise HTTPException(status_code=401, detail="invalid credentials")

    return {"status": "OK"}

@app.post("/request-reset")
def request_reset(r: ResetRequest):
    token = str(uuid.uuid4())
    expires = datetime.datetime.utcnow() + datetime.timedelta(hours=1)

    with db() as conn, conn.cursor() as cur:
        cur.execute("""
            UPDATE users
               SET reset_token = %s,
                   reset_expires = %s
             WHERE username = %s;
        """, (token, expires, r.username))

    reset_link = f"http://localhost:5173/?view=reset&token={token}"
    return {"reset_link": reset_link}

@app.post("/reset-password")
def reset_password(r: ResetRequest):
    # 1) Vérifier le token
    with db() as conn, conn.cursor() as cur:
        cur.execute("""
            SELECT username FROM users
             WHERE reset_token = %s
               AND reset_expires > NOW();
        """, (r.username,))  # on passe simplement username=token
        row = cur.fetchone()
    if not row:
        raise HTTPException(status_code=400, detail="token invalide ou expiré")

    username = row[0]

    # 2) Générer nouveau mot de passe comme dans genpwd()
    pwd = ''.join(secrets.choice(ALPHA) for _ in range(24))
    pwd_hash = bcrypt.hash(pwd)
    img = io.BytesIO()
    qrcode.make(pwd).save(img, 'PNG')

    # 3) Mettre à jour en base
    with db() as conn, conn.cursor() as cur:
        cur.execute("""
            UPDATE users
               SET password_hash = %s,
                   gendate = NOW(),
                   expired = false,
                   reset_token = NULL,
                   reset_expires = NULL
             WHERE username = %s;
        """, (pwd_hash, username))

    return {
        "password": pwd,
        "password_qr": base64.b64encode(img.getvalue()).decode()
    }
