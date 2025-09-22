from fastapi.testclient import TestClient
from app.main import app
import os

client = TestClient(app)

def test_health():
    res = client.get('/health')
    assert res.status_code == 200
    assert res.json() == {'status': 'ok'}

# The DB-dependent tests are marked as integration and require DB env vars to be set.
