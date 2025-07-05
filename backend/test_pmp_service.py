"""
Unit and integration tests for PMP Backend (SAFE AI, stateless, and owner-controlled)
"""
from fastapi.testclient import TestClient
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
from pmp_service import app
import starlette
import starlette.testclient
import inspect
print('DIAG: starlette version:', getattr(starlette, '__version__', 'unknown'))
import inspect
print('DIAG: TestClient type:', type(TestClient))
print('DIAG: TestClient module:', TestClient.__module__)
print('DIAG: starlette.testclient file:', inspect.getfile(starlette.testclient))
print('DIAG: TestClient file:', inspect.getfile(TestClient))
# Print constructor signatures
print('DIAG: TestClient.__init__ signature:', inspect.signature(TestClient.__init__))
try:
    from starlette.testclient import Client as StarletteClient
    print('DIAG: StarletteClient.__init__ signature:', inspect.signature(StarletteClient.__init__))
except Exception as e:
    print('DIAG: Could not inspect StarletteClient.__init__:', e)
client = TestClient(app)  # Correct usage: positional argument only, no keyword
print('DIAG: client type:', type(client))
print('DIAG: client module:', type(client).__module__)

def test_authenticate_success():
    resp = client.post("/auth/verify", json={
        "face3d": "OWNER_FACE_3D",
        "passcode": "SuperSecretPasscode1",
        "biometric": "OWNER_BIOMETRIC",
        "behavioral": "OWNER_BEHAVIOR"
    })
    assert resp.status_code == 200
    assert resp.json()["status"] == "authenticated"

def test_authenticate_failure():
    resp = client.post("/auth/verify", json={
        "face3d": "WRONG",
        "passcode": "short",
        "biometric": "WRONG",
        "behavioral": "WRONG"
    })
    assert resp.status_code == 403

def test_content_generation_stub():
    resp = client.post("/content/generate", json={
        "type": "text",
        "prompt": "Test prompt",
        "preferences": {"kink": "roleplay"}
    })
    assert resp.status_code == 200
    assert "8K text" in resp.json()["result"]

def test_feedback_stub():
    resp = client.post("/feedback", json={
        "session_id": "test-session",
        "feedback": "hot"
    })
    assert resp.status_code == 200
    assert resp.json()["status"].startswith("feedback received")

def test_kink_suggestions():
    resp = client.get("/kinks/suggest")
    assert resp.status_code == 200
    assert "suggestions" in resp.json()

def test_security_status():
    resp = client.get("/security/status")
    assert resp.status_code == 200
    assert resp.json()["encryption"].startswith("quantum")

def test_health():
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"
