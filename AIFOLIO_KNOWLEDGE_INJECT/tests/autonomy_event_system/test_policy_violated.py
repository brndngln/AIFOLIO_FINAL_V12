from autonomy.pipeline.event_bus import dispatch_event


def test_policy_violated_event(monkeypatch):
    events = []

    def fake_log_vault_event(vault_id, event_type, payload, errors):
        events.append((event_type, payload))

    monkeypatch.setattr(
        "autonomy.pipeline.listeners.policy_violated.log_vault_event",
        fake_log_vault_event,
    )
    payload = {
        "vault_id": "V789",
        "policy_name": "No Export",
        "owner_email": "user@example.com",
        "alert_email_opt_in": True,
    }
    dispatch_event("policy_violated", payload)
    assert events, "Event should be logged"
    assert events[0][0] == "policy_violated"
    assert "ai_results" in events[0][1]
