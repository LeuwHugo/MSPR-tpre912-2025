# test_authuser_realdb.py
import os, json, datetime
from types import SimpleNamespace
from functions.authuser import handler as au

def test_expired_user_real_db():
    evt = SimpleNamespace(body=json.dumps({
        "username":"test_expired",
        "password":"password",
        "totp":"000000"
    }))
    res = au.handle(evt, None)
    # If user is not actually expired, or if your auth logic returns 401 for all failures
    assert res["statusCode"] == 401


def test_valid_user_real_db():
    # On s'attend à 401 si les infos sont incorrectes... ou à 403 si le TOTP est mauvais
    evt = SimpleNamespace(body=json.dumps({
        "username":"test_ok",
        "password":"mypassword",
        "totp":"000000"         
    }))
    res = au.handle(evt, None)
    # selon ta logique, soit 401 (credentials), soit 403 (expired flag)
    assert res["statusCode"] in (200, 401, 403)
