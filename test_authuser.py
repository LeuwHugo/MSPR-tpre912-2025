# tests/test_authuser.py
import json
import datetime
from types import SimpleNamespace
from importlib import reload
import functions.authuser.handler as au

def test_expired_user(monkeypatch):
    past = datetime.datetime.utcnow() - datetime.timedelta(days=190)
    # Hash pour le password "x" avec bcrypt (vous devrez ajuster selon votre implémentation)
    password_hash = "$2b$12$fake.hash.for.testing.purposes.only"  
    fake_row = (password_hash, "BASE32SECRET", past, False)

    # Créer une classe spécifique pour ce test qui retourne fake_row
    class TestSpecificConnection:
        def __init__(self):
            pass
        
        def _create_cursor(self):
            class TestCursor:
                def execute(self, *args, **kwargs): 
                    pass
                def fetchone(self): 
                    return fake_row  # Retourne les données du test
                def __enter__(self):
                    return self
                def __exit__(self, exc_type, exc_val, exc_tb):
                    pass
            return TestCursor()
        
        def cursor(self):
            return self._create_cursor()
        
        def __enter__(self):
            return self
        
        def __exit__(self, exc_type, exc_val, exc_tb):
            pass

    def test_fake_conn():
        return TestSpecificConnection()
    
    # Patch avec notre connexion spécifique pour ce test
    monkeypatch.setattr("functions.common.db.get_conn", test_fake_conn)
    
    # Reload pour prendre en compte le patch
    reload(au)

    evt = SimpleNamespace(body=json.dumps(
        {"username":"alice","password":"x","totp":"000000"}))
    
    result = au.handle(evt, None)
    assert result["statusCode"] == 403