# TEST: test_gen2fa.py
import json, base64
from types import SimpleNamespace
from functions.gen2fa import handler as g2
def test_secret_and_qr():
    evt = SimpleNamespace(body=json.dumps({"username":"alice"}))
    res = g2.handle(evt, None)
    data = json.loads(res["body"])

    assert res["statusCode"] == 200
    assert len(data["secret"]) == 32           # base32 size
    base64.b64decode(data["secret_qr"])
