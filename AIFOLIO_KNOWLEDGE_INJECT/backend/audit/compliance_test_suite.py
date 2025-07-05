import requests
import json
from datetime import datetime

API_BASE = "http://localhost:8000/api"
ADMIN_ID = "admin_demo"
MFA_CODE = "000000"  # Replace with a real TOTP code for live test


def log(msg):
    print(f"[COMPLIANCE TEST] {datetime.utcnow().isoformat()} - {msg}")


def test_manual_override():
    log("Testing manual override with invalid MFA...")
    r = requests.post(
        f"{API_BASE}/rotation/manual_override",
        json={"adminId": ADMIN_ID, "code": "123456"},  # Invalid code
    )
    assert r.status_code == 401, "Manual override should fail with bad MFA"
    log("Manual override correctly rejected with invalid MFA.")

    log("Testing manual override with valid MFA...")
    r = requests.post(
        f"{API_BASE}/rotation/manual_override",
        json={"adminId": ADMIN_ID, "code": MFA_CODE},
    )
    assert r.status_code == 200 and r.json().get(
        "success"
    ), "Manual override should succeed with valid MFA"
    log("Manual override succeeded with valid MFA.")


def test_freeze_toggle():
    log("Testing freeze toggle (pause)...")
    r = requests.post(
        f"{API_BASE}/rotation/toggle",
        json={"adminId": ADMIN_ID, "code": MFA_CODE, "enabled": False},
    )
    assert r.status_code == 200 and not r.json().get(
        "enabled"
    ), "Freeze should set enabled to False"
    log("Rotation freeze activated.")

    log("Testing freeze toggle (resume)...")
    r = requests.post(
        f"{API_BASE}/rotation/toggle",
        json={"adminId": ADMIN_ID, "code": MFA_CODE, "enabled": True},
    )
    assert r.status_code == 200 and r.json().get(
        "enabled"
    ), "Unfreeze should set enabled to True"
    log("Rotation resumed.")


def test_usage_monitor():
    log("Fetching usage metrics...")
    r = requests.get(f"{API_BASE}/usage/metrics")
    assert r.status_code == 200
    log(f"Usage metrics: {json.dumps(r.json())}")

    log("Fetching usage anomalies...")
    r = requests.get(f"{API_BASE}/usage/anomalies")
    assert r.status_code == 200
    log(f"Usage anomalies: {json.dumps(r.json())}")

    log("Toggling auto-freeze...")
    r = requests.post(f"{API_BASE}/usage/auto-freeze", json={"enable": True})
    assert r.status_code == 200 and r.json().get("auto_freeze")
    log("Auto-freeze enabled.")
    r = requests.post(f"{API_BASE}/usage/auto-freeze", json={"enable": False})
    assert r.status_code == 200 and not r.json().get("auto_freeze")
    log("Auto-freeze disabled.")


def run_all():
    log("--- Starting Compliance Test Suite ---")
    test_manual_override()
    test_freeze_toggle()
    test_usage_monitor()
    log("--- Compliance Test Suite Completed ---")


if __name__ == "__main__":
    run_all()
