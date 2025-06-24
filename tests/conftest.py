# tests/conftest.py
import sys, types, contextlib
import pytest
from importlib import reload

class FakeConnection:
    """Simule une connexion de base de données avec le protocole context manager"""
    def __init__(self):
        pass
    
    def _create_cursor(self):
        class FakeCursor:
            def execute(self, *args, **kwargs): 
                pass
            def fetchone(self): 
                return None
            def fetchall(self):
                return []
            def __enter__(self):
                return self
            def __exit__(self, exc_type, exc_val, exc_tb):
                pass
        return FakeCursor()
    
    def cursor(self):
        return self._create_cursor()
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

def _fake_conn():
    """Retourne une fausse connexion qui supporte le protocole context manager"""
    return FakeConnection()

@pytest.fixture(autouse=True)
def stub_db(monkeypatch):
    """
    Stub la fonction get_conn() pour empêcher tout vrai appel à psycopg2.connect().
    """
    # Patch the get_conn function in the common.db module before any imports
    monkeypatch.setattr("functions.common.db.get_conn", _fake_conn)
    
    # Also patch psycopg2.connect directly as a fallback
    try:
        import psycopg2
        monkeypatch.setattr(psycopg2, "connect", lambda *args, **kwargs: FakeConnection())
    except ImportError:
        pass