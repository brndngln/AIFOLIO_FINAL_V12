import os
import json
import time
import logging
import traceback
from datetime import datetime
from autonomy.utils.dashboard_push import push_dashboard_update
from autonomy.utils.slack_alert import send_slack_alert
from autonomy.utils.telegram_alert import send_telegram_alert
from autonomy.utils.email_alert import send_email_alert
from autonomy.utils.vault_event_log import log_vault_event
from autonomy.utils.activity_log import log_activity
from autonomy.ai_tools.anomaly_detector import detect_anomaly
from autonomy.ai_tools.audit_bot import audit_vault_compliance
from autonomy.utils.retry import retry_safe

logger = logging.getLogger("vault_refunded")

@retry_safe(max_attempts=3, backoff_factor=2)
def push_dashboard(vault_id, payload):
    push_dashboard_update(vault_id, payload)

@retry_safe(max_attempts=3, backoff_factor=2)
def send_alerts(payload, event_type, error=None):
    alert_msg = f"Vault {event_type}: {payload.get('vault_id', 'N/A')} (Buyer: {payload.get('buyer_email', 'N/A')})"
    if error:
        alert_msg += f"\nError: {error}"
    send_slack_alert(alert_msg)
    send_telegram_alert(alert_msg)
    if payload.get("alert_email_opt_in"):
        send_email_alert(payload.get("owner_email"), alert_msg)

@retry_safe(max_attempts=3, backoff_factor=2)
def audit_vault(payload):
    audit_vault_compliance(payload.get("vault_path", ""), payload)


def handle_event(payload: dict):
    """
    Handles the 'vault_refunded' event with SAFE AI, retry-safe integrations, and robust logging.
    """
    vault_id = payload.get("vault_id")
    buyer_email = payload.get("buyer_email")
    analytics_log = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../analytics/refund_log.json'))
    errors = []
    start_time = time.time()
    entry = {
        "event": "vault_refunded",
        "timestamp": datetime.utcnow().isoformat(),
        "vault_id": vault_id,
        "buyer_email": buyer_email,
        "reason": payload.get("reason", "N/A")
    }
    # Log refund event
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
        logger.error(f"Failed to log refund event: {e}\n{traceback.format_exc()}")
        errors.append(f"Log: {e}")
        send_alerts(payload, "refunded", error=str(e))
    # Dashboard update (flag as refunded)
    try:
        push_dashboard(vault_id, payload)
    except Exception as e:
        logger.error(f"Dashboard update failed: {e}\n{traceback.format_exc()}")
        errors.append(f"Dashboard: {e}")
    # --- SAFE FILENAME SANITIZATION & EMAIL DELIVERY ---
    from autonomy.vaults.filename_sanitizer import enforce_safe_filename
    from autonomy.notifications.email_engine import send_vault_email
    try:
        attachments = []
        refund_receipt = payload.get('refund_receipt_path', 'refund_receipt.pdf')
        refund_policy = payload.get('refund_policy_path', 'refund_policy.pdf')
        for file_path in [refund_receipt, refund_policy]:
            safe_path = enforce_safe_filename(file_path, payload.get('vault_title', payload.get('vault_id', 'refund')))
            attachments.append(safe_path)
        email_subject = f"[AIFOLIO] Vault Refunded: {payload.get('vault_id', '')}"
        email_body = "Your vault refund has been processed. Your refund receipt and policy are attached."
        send_status = send_vault_email(
            payload.get('buyer_email') or payload.get('email'),
            email_subject,
            email_body,
            attachments
        )
    except Exception as e:
        logger.error(f"Refund email/attachment delivery failed: {e}\n{traceback.format_exc()}")
        errors.append(f"Email: {e}")
    # Audit compliance
    try:
        audit_vault(payload)
    except Exception as e:
        logger.error(f"Audit compliance failed: {e}\n{traceback.format_exc()}")
        errors.append(f"Audit: {e}")
    # Alerts (confirmation email, Slack, Telegram)
    try:
        send_alerts(payload, "refunded")
    except Exception as e:
        logger.error(f"Alert failed: {e}\n{traceback.format_exc()}")
        errors.append(f"Alert: {e}")
    # Log to vault event log/activity log
    try:
        log_vault_event(vault_id, "vault_refunded", payload, errors)
        log_activity(vault_id, "vault_refunded", payload, errors)
    except Exception as e:
        logger.error(f"Vault activity logging failed: {e}\n{traceback.format_exc()}")
        errors.append(f"VaultLog: {e}")
    # AI anomaly detection on failures
    if errors:
        try:
            detect_anomaly(vault_id, errors)
        except Exception as e:
            logger.error(f"Anomaly detection failed: {e}\n{traceback.format_exc()}")
    print(f"[AIFOLIO] Refunded vault {vault_id} for {buyer_email}. Dashboard flagged. Confirmation email sent.")
    return {"status": "success", "vault_id": vault_id, "buyer_email": buyer_email, "errors": errors}
