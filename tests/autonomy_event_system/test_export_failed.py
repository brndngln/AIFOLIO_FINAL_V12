import os
import json
import tempfile
from autonomy.pipeline.listeners import export_failed

def test_export_failed_event(monkeypatch):
    payload = {
        "vault_id": "testvault4",
        "vault_path": "vaults/testvault4",
        "alert_email_opt_in": False
    }
    with tempfile.TemporaryDirectory() as tmpdir:
        monkeypatch.setattr(export_failed, "push_dashboard_update", lambda *a, **kw: None)
        monkeypatch.setattr(export_failed, "send_alert", lambda *a, **kw: None)
        monkeypatch.setattr(export_failed, "send_slack_alert", lambda *a, **kw: None)
        monkeypatch.setattr(export_failed, "send_telegram_alert", lambda *a, **kw: None)
        monkeypatch.setattr(export_failed, "send_email_alert", lambda *a, **kw: None)
        monkeypatch.setattr(export_failed, "log_vault_event", lambda *a, **kw: None)
        monkeypatch.setattr(export_failed, "log_activity", lambda *a, **kw: None)
        monkeypatch.setattr(export_failed, "detect_anomaly", lambda *a, **kw: None)
        monkeypatch.setattr(export_failed, "check_vault_metadata", lambda *a, **kw: {'compliant': True, 'missing': [], 'invalid': []})
        # Patch analytics log path
        monkeypatch.setattr(export_failed, "os", os)
        monkeypatch.setattr(export_failed, "json", json)
        # Actually run the event
        result = export_failed.handle_event(payload)
        assert result["status"] == "success" or result is None
