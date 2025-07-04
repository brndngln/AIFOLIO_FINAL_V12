import os
import json
from datetime import datetime

<<<<<<< HEAD
import os
import json
import time
import logging
import traceback
from datetime import datetime
=======
import time
>>>>>>> omni_repair_backup_20250704_1335
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
    Handles the 'upsell_triggered' event with SAFE AI, retry-safe integrations, and robust logging.
    """
    errors = []
    start_time = time.time()
    user_id = payload.get("user_id")
    vault_id = payload.get("vault_id")
    upsell_page = payload.get("upsell_page")
    bonus_delivered = payload.get("bonus_delivered", False)
    analytics_log = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../analytics/upsell_log.json'))
    entry = {
        "event": "upsell_triggered",
        "timestamp": datetime.utcnow().isoformat(),
        "user_id": user_id,
        "vault_id": vault_id,
        "upsell_page": upsell_page,
        "bonus_delivered": bonus_delivered
    }
    # Log upsell event
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
        push_dashboard_update(vault_id, payload)
    except Exception as e:
        errors.append(f"Dashboard: {e}")
    # --- SAFE FILENAME SANITIZATION & NOTIFICATION (if applicable) ---
    from autonomy.vaults.filename_sanitizer import enforce_safe_filename
    from autonomy.notifications.email_engine import send_vault_email
    try:
        if payload.get('bonus_file_path'):
            safe_path = enforce_safe_filename(payload['bonus_file_path'], payload.get('vault_title', vault_id))
            if payload.get('notify_on_bonus'):
                email_subject = f"[AIFOLIO] Upsell Bonus Delivered: {vault_id}"
<<<<<<< HEAD
                email_body = f"A bonus file for your upsell was delivered."
=======
                email_body = "A bonus file for your upsell was delivered."
>>>>>>> omni_repair_backup_20250704_1335
                send_status = send_vault_email(
                    payload.get('user_email'),
                    email_subject,
                    email_body,
                    [safe_path]
                )
    except Exception as e:
        errors.append(f"Notify: {e}")
    # Audit
    try:
        audit_vault_compliance(payload.get("vault_path", ""), payload)
    except Exception as e:
        errors.append(f"Audit: {e}")
    # Alerts
    try:
        msg = f"Upsell triggered for vault {vault_id} by user {user_id} on page {upsell_page}. Bonus delivered: {bonus_delivered}"
        send_slack_alert(msg)
        send_telegram_alert(msg)
        if payload.get("alert_email_opt_in"):
            send_email_alert(payload.get("owner_email"), msg)
    except Exception as e:
        errors.append(f"Alert: {e}")
    # Log to event/activity log
    try:
        log_vault_event(vault_id, "upsell_triggered", payload, errors)
        log_activity(vault_id, "upsell_triggered", payload, errors)
    except Exception as e:
        errors.append(f"VaultLog: {e}")
    # AI anomaly detection on failures
    if errors:
        try:
            detect_anomaly(vault_id, errors)
<<<<<<< HEAD
        except Exception as e:
=======
        except Exception:
>>>>>>> omni_repair_backup_20250704_1335
            pass
    print(f"[AIFOLIO] Upsell triggered for vault {vault_id} by user {user_id} on page {upsell_page}. Bonus delivered: {bonus_delivered}")
    return {"status": "success", "vault_id": vault_id, "user_id": user_id, "errors": errors}
