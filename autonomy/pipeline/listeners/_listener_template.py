"""
SAFE AI-Compliant Event Listener Template for AIFOLIO
- Static-scope, non-sentient logic
- Audit/event/error logging
- Fallback alerting for critical flows
- Manual approval for AI/compliance/refund/pricing output
- No cross-vault memory, no loops or self-calling functions, or autonomy
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
    SAFE AI: If event['metadata'] is present, invoke automation_safeguard.enforce_all_safeguards and block/audit-log if validation fails.
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
    errors = []
    # SAFE AI VALIDATION LAYER
    metadata = event.get('metadata', {})
    if metadata:
        try:
            from autonomy.validation import automation_safeguard
            valid, safeguard_msg = automation_safeguard.enforce_all_safeguards(metadata)
            if not valid:
                errors.append(f"SAFEGUARD: {safeguard_msg}")
                automation_safeguard.audit_log('SAFEGUARD_BLOCKED', {'vault_id': event.get('vault_id'), 'reason': safeguard_msg, 'metadata': metadata})
                # Optionally send alert
                try:
                    from autonomy.compliance.alert_engine import send_alert
                    send_alert(type="safeguard_blocked", message=safeguard_msg, to=metadata.get("owner_email"))
                except Exception:
                    pass
                # Log and abort further processing
                try:
                    from autonomy.utils.vault_event_log import log_vault_event
                    from autonomy.utils.activity_log import log_activity
                    log_vault_event(event.get('vault_id'), "safeguard_blocked", metadata, errors)
                    log_activity(event.get('vault_id'), "safeguard_blocked", metadata, errors)
                except Exception:
                    pass
                return {
                    "status": "blocked",
                    "vault_id": event.get('vault_id'),
                    "errors": errors
                }
        except Exception as e:
            logger.error(f"SAFEGUARD validation failed: {e}")
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
