from autonomy.pipeline.event_bus import dispatch_event


def test_refund_issued_event(monkeypatch):
    events = []

    def fake_log_vault_event(vault_id, event_type, payload, errors):
        events.append((event_type, payload))

    monkeypatch.setattr(
        "autonomy.pipeline.listeners.refund_issued.log_vault_event",
        fake_log_vault_event,
    )
    payload = {
        "vault_id": "V123",
        "refund_amount": 10.0,
        "owner_email": "user@example.com",
        "alert_email_opt_in": True,
    }
    dispatch_event("refund_issued", payload)
    assert events, "Event should be logged"
    assert events[0][0] == "refund_issued"
    assert "ai_results" in events[0][1]
