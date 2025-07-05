import os
import json
import tempfile
from autonomy.pipeline.listeners import vault_fulfilled


def test_vault_fulfilled_event(monkeypatch):
    payload = {
        "vault_id": "testvault1",
        "buyer_email": "buyer@example.com",
        "vault_path": "vaults/testvault1",
        "alert_email_opt_in": False,
    }
    with tempfile.TemporaryDirectory() as tmpdir:
        monkeypatch.setattr(
            vault_fulfilled, "logger", type("FakeLogger", (), {"error": print})()
        )
        monkeypatch.setattr(vault_fulfilled, "push_dashboard", lambda *a, **kw: None)
        monkeypatch.setattr(vault_fulfilled, "send_alerts", lambda *a, **kw: None)
        monkeypatch.setattr(vault_fulfilled, "audit_vault", lambda *a, **kw: None)
        monkeypatch.setattr(vault_fulfilled, "log_vault_event", lambda *a, **kw: None)
        monkeypatch.setattr(vault_fulfilled, "log_activity", lambda *a, **kw: None)
        monkeypatch.setattr(vault_fulfilled, "detect_anomaly", lambda *a, **kw: None)
        # Patch analytics log path
        monkeypatch.setattr(vault_fulfilled, "os", os)
        monkeypatch.setattr(vault_fulfilled, "json", json)
        # Actually run the event
        result = vault_fulfilled.handle_event(payload)
        assert result["status"] == "success"
        assert result["vault_id"] == "testvault1"
