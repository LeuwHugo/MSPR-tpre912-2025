# TEST: test_genpwd.py
import json, base64, re
from types import SimpleNamespace
from functions.genpwd import handler as gp

class Event(SimpleNamespace): pass             # wrapper minimal

def test_password_generated():
    evt = Event(body=json.dumps({"username":"alice"}))
    res = gp.handle(evt, None)
    data = json.loads(res["body"])

    assert res["statusCode"] == 200
    assert len(data["password"]) == 24
    # Accepter tous les caractères imprimables ASCII
    assert re.fullmatch(r"[ -~]{24}", data["password"])
    # QR doit être du Base64 valide
    base64.b64decode(data["password_qr"])