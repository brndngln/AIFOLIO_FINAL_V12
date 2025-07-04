<<<<<<< HEAD
import pytest
=======
>>>>>>> omni_repair_backup_20250704_1335
from autonomy.pipeline.event_bus import dispatch_event

def test_download_initiated_event(monkeypatch):
    events = []
    def fake_log_vault_event(vault_id, event_type, payload, errors):
        events.append((event_type, payload))
    monkeypatch.setattr('autonomy.pipeline.listeners.download_initiated.log_vault_event', fake_log_vault_event)
    payload = {
        'vault_id': 'V456',
        'download_url': 'https://example.com/file.pdf',
        'owner_email': 'user@example.com',
        'alert_email_opt_in': True
    }
<<<<<<< HEAD
    from autonomy.pipeline.event_bus import dispatch_event
=======
>>>>>>> omni_repair_backup_20250704_1335
    dispatch_event('download_initiated', payload)
    assert events, 'Event should be logged'
    assert events[0][0] == 'download_initiated'
    assert 'ai_results' in events[0][1]
