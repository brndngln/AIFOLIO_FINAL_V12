import os
import json
import tempfile
from autonomy.pipeline.listeners import vault_sold


def test_vault_sold_event(monkeypatch):
    payload = {
        "vault_id": "testvault5",
        "email": "buyer5@example.com",
        "country": "US",
        "vault_path": "vaults/testvault5",
        "alert_email_opt_in": True,
    }
    with tempfile.TemporaryDirectory() as tmpdir:
        monkeypatch.setattr(
            vault_sold,
            "logger",
            type("FakeLogger", (), {"error": print, "warning": print})(),
        )
        monkeypatch.setattr(vault_sold, "push_dashboard", lambda *a, **kw: None)
        monkeypatch.setattr(vault_sold, "send_alerts", lambda *a, **kw: None)
        monkeypatch.setattr(vault_sold, "audit_vault", lambda *a, **kw: None)
        monkeypatch.setattr(vault_sold, "log_vault_event", lambda *a, **kw: None)
        monkeypatch.setattr(vault_sold, "log_activity", lambda *a, **kw: None)
        monkeypatch.setattr(vault_sold, "detect_anomaly", lambda *a, **kw: None)
        monkeypatch.setattr(vault_sold, "export_to_pdf", lambda *a, **kw: None)
        monkeypatch.setattr(vault_sold, "send_alert", lambda *a, **kw: None)
        monkeypatch.setattr(
            vault_sold, "trigger_compliance_workflow", lambda *a, **kw: None
        )
        # Patch analytics log path
        monkeypatch.setattr(vault_sold, "os", os)
        monkeypatch.setattr(vault_sold, "json", json)
        # Actually run the event
        result = vault_sold.handle_event(payload)
        assert result["status"] == "success"
        assert result["vault_id"] == "testvault5"
