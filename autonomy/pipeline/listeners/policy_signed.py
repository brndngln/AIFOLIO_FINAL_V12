import os
import json
from datetime import datetime

import time
from autonomy.utils.dashboard_push import push_dashboard_update
from autonomy.utils.slack_alert import send_slack_alert
from autonomy.utils.telegram_alert import send_telegram_alert
from autonomy.utils.email_alert import send_email_alert
from autonomy.utils.vault_event_log import log_vault_event
from autonomy.utils.activity_log import log_activity
from autonomy.ai_tools.anomaly_detector import detect_anomaly
from autonomy.ai_tools.audit_bot import audit_vault_compliance

def handle_event(payload: dict):
    """
    Handles the 'policy_signed' event with SAFE AI, retry-safe integrations, and robust logging.
    """
    errors = []
    start_time = time.time()
    user_id = payload.get("user_id")
    policy_version = payload.get("policy_version")
    analytics_log = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../analytics/policy_sign_log.json'))
    entry = {
        "event": "policy_signed",
        "timestamp": datetime.utcnow().isoformat(),
        "user_id": user_id,
        "policy_version": policy_version
    }
    # Log policy signature
    try:
        if os.path.exists(analytics_log):
            with open(analytics_log, "r+") as f:
                logs = json.load(f)
                logs.append(entry)
                f.seek(0)
                json.dump(logs, f, indent=2)
        else:
            with open(analytics_log, "w") as f:
                json.dump([entry], f, indent=2)
    except Exception as e:
        errors.append(f"Log: {e}")
    # Dashboard update
    try:
        push_dashboard_update(user_id, payload)
    except Exception as e:
        errors.append(f"Dashboard: {e}")
    # Audit
    try:
        audit_vault_compliance(payload.get("vault_path", ""), payload)
    except Exception as e:
        errors.append(f"Audit: {e}")
    # Alerts
    try:
        msg = f"Policy version {policy_version} signed by user {user_id}."
        send_slack_alert(msg)
        send_telegram_alert(msg)
        if payload.get("alert_email_opt_in"):
            send_email_alert(payload.get("owner_email"), msg)
    except Exception as e:
        errors.append(f"Alert: {e}")
    # Log to event/activity log
    try:
        log_vault_event(user_id, "policy_signed", payload, errors)
        log_activity(user_id, "policy_signed", payload, errors)
    except Exception as e:
        errors.append(f"VaultLog: {e}")
    # AI anomaly detection on failures
    if errors:
        try:
            detect_anomaly(user_id, errors)
        except Exception:
            pass
    print(f"[AIFOLIO] Policy version {policy_version} signed by user {user_id}.")
    return {"status": "success", "user_id": user_id, "errors": errors}
