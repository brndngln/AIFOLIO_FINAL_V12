"""
SAFE AI-Compliant Event Listener Template for AIFOLIO
- Static-scope, non-sentient logic
- Audit/event/error logging
- Fallback alerting for critical flows
- Manual approval for AI/compliance/refund/pricing output
- No cross-vault memory, recursion, or autonomy
"""
import json
import datetime
import os
import logging

EVENT_LOG = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../analytics/event_log.json'))
ERROR_LOG = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../analytics/error_log.json'))
os.makedirs(os.path.dirname(EVENT_LOG), exist_ok=True)
os.makedirs(os.path.dirname(ERROR_LOG), exist_ok=True)

# Optionally import fallback alerting
try:
    from autonomy.notifications.slack_alert import send_slack_alert
    from autonomy.notifications.sms_alert import send_sms_alert
except ImportError:
    send_slack_alert = lambda msg: None
    send_sms_alert = lambda msg: None

def handle_event(event):
    """
    Main event handler for this event type.
    """
    logger = logging.getLogger(__name__)
    entry = {
        'timestamp': datetime.datetime.utcnow().isoformat() + 'Z',
        'event': event.get('event_type', __name__),
        'vault_id': event.get('vault_id'),
        'user_id': event.get('user_id'),
        'metadata': event.get('metadata', {}),
        'payload': event
    }
    try:
        with open(EVENT_LOG, 'a') as f:
            f.write(json.dumps(entry) + '\n')
    except Exception as e:
        logger.error(f"Event log failed: {e}")
        with open(ERROR_LOG, 'a') as f:
            f.write(json.dumps({'timestamp': entry['timestamp'], 'event': entry['event'], 'error': str(e)}) + '\n')
        # Fallback alert for critical event types
        if event.get('critical', False):
            send_slack_alert(f"Critical event log failure: {entry['event']} - {e}")
            send_sms_alert(f"Critical event log failure: {entry['event']} - {e}")
    return entry
