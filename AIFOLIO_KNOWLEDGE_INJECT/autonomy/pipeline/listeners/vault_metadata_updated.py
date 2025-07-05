import os
import json
from datetime import datetime

import time
import logging
import traceback
from autonomy.integrations.stripe_sync import sync_to_stripe
from autonomy.integrations.notion_sync import sync_to_notion
from autonomy.integrations.crm_sync import sync_to_crm
from autonomy.integrations.analytics_reporting import report_to_analytics
from autonomy.integrations.xbrl_export import export_to_xbrl
from autonomy.ai_tools.spellcheck import spellcheck_text
from autonomy.ai_tools.grammar_check import grammar_check_text
from autonomy.ai_tools.audit_bot import audit_vault_compliance
from autonomy.utils.dashboard_push import push_dashboard_update
from autonomy.utils.slack_alert import send_slack_alert
from autonomy.utils.telegram_alert import send_telegram_alert
from autonomy.utils.email_alert import send_email_alert
from autonomy.utils.performance_monitor import monitor_vault_build
from autonomy.utils.version_tracker import track_template_version
from autonomy.utils.retry import retry_safe

logger = logging.getLogger("vault_metadata_updated")


@retry_safe(max_attempts=3, backoff_factor=2)
def sync_integrations(payload):
    sync_to_stripe(payload)
    sync_to_notion(payload)
    sync_to_crm(payload)
    report_to_analytics(payload)
    export_to_xbrl(payload)


@retry_safe(max_attempts=3, backoff_factor=2)
def send_alerts(payload, event_type, error=None):
    alert_msg = f"Vault {event_type}: {payload.get('vault_id', 'N/A')} (User: {payload.get('user_id', 'N/A')})"
    if error:
        alert_msg += f"\nError: {error}"
    send_slack_alert(alert_msg)
    send_telegram_alert(alert_msg)
    if payload.get("alert_email_opt_in"):
        send_email_alert(payload.get("owner_email"), alert_msg)


@retry_safe(max_attempts=3, backoff_factor=2)
def push_dashboard(vault_id, payload):
    push_dashboard_update(vault_id, payload)


@retry_safe(max_attempts=3, backoff_factor=2)
def audit_and_monitor(payload):
    audit_vault_compliance(payload.get("vault_path", ""), payload)
    monitor_vault_build(payload.get("vault_path", ""), payload)
    track_template_version(payload.get("vault_path", ""), payload)


def handle_event(payload: dict):
    """
    Handles the 'vault_metadata_updated' event with SAFE AI, retry-safe integrations, and robust logging.
    """
    from autonomy.validation import automation_safeguard

    vault_id = payload.get("vault_id")
    errors = []
    valid, safeguard_msg = automation_safeguard.enforce_all_safeguards(payload)
    if not valid:
        import logging

        logger = logging.getLogger("vault_metadata_updated")
        logger.error(f"SAFEGUARD BLOCK: {safeguard_msg}")
        errors.append(f"SAFEGUARD: {safeguard_msg}")
        automation_safeguard.audit_log(
            "SAFEGUARD_BLOCKED",
            {"vault_id": vault_id, "reason": safeguard_msg, "payload": payload},
        )
        # Optionally send alert
        try:
            from autonomy.compliance.alert_engine import send_alert

            send_alert(
                type="safeguard_blocked",
                message=safeguard_msg,
                to=payload.get("owner_email"),
            )
        except Exception:
            pass
        # Log and abort further processing
        from autonomy.utils.vault_event_log import log_vault_event
        from autonomy.utils.activity_log import log_activity

        log_vault_event(vault_id, "safeguard_blocked", payload, errors)
        log_activity(vault_id, "safeguard_blocked", payload, errors)
        return {"status": "blocked", "vault_id": vault_id, "errors": errors}
    user_id = payload.get("user_id")
    changes = payload.get("changes")
    analytics_log = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__), "../../analytics/metadata_update_log.json"
        )
    )
    start_time = time.time()
    # Spellcheck/grammar correction for changed fields
    if isinstance(changes, dict):
        for k, v in changes.items():
            if isinstance(v, str):
                v = spellcheck_text(grammar_check_text(v))
                changes[k] = v
    entry = {
        "event": "vault_metadata_updated",
        "timestamp": datetime.utcnow().isoformat(),
        "vault_id": vault_id,
        "user_id": user_id,
        "changes": changes,
    }
    import os
    import logging

    logger = logging.getLogger("vault_metadata_updated")
    # Log metadata change
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
        logger.error(f"Failed to log metadata update: {e}\n{traceback.format_exc()}")
        errors.append(f"Log: {e}")
        from autonomy.utils.slack_alert import send_slack_alert
        from autonomy.utils.telegram_alert import send_telegram_alert
        from autonomy.utils.email_alert import send_email_alert

        send_slack_alert(str(e))
        send_telegram_alert(str(e))
        if payload.get("alert_email_opt_in"):
            send_email_alert(payload.get("owner_email"), str(e))
    # Integrations (Stripe, Notion, CRM, Analytics, XBRL)
    try:
        from autonomy.integrations.stripe_sync import sync_to_stripe
        from autonomy.integrations.notion_sync import sync_to_notion
        from autonomy.integrations.crm_sync import sync_to_crm
        from autonomy.integrations.analytics_reporting import report_to_analytics
        from autonomy.integrations.xbrl_export import export_to_xbrl

        sync_to_stripe(payload)
        sync_to_notion(payload)
        sync_to_crm(payload)
        report_to_analytics(payload)
        export_to_xbrl(payload)
    except Exception as e:
        logger.error(f"Integration sync failed: {e}\n{traceback.format_exc()}")
        errors.append(f"Integration: {e}")
        from autonomy.utils.slack_alert import send_slack_alert
        from autonomy.utils.telegram_alert import send_telegram_alert
        from autonomy.utils.email_alert import send_email_alert

        send_slack_alert(str(e))
        send_telegram_alert(str(e))
        if payload.get("alert_email_opt_in"):
            send_email_alert(payload.get("owner_email"), str(e))
    # Dashboard update
    try:
        from autonomy.utils.dashboard_push import push_dashboard_update

        push_dashboard_update(vault_id, payload)
    except Exception as e:
        logger.error(f"Dashboard update failed: {e}\n{traceback.format_exc()}")
        errors.append(f"Dashboard: {e}")
    # Audit, monitor, version tracking
    try:
        from autonomy.ai_tools.audit_bot import audit_vault_compliance
        from autonomy.utils.performance_monitor import monitor_vault_build
        from autonomy.utils.version_tracker import track_template_version

        audit_vault_compliance(payload.get("vault_path", ""), payload)
        monitor_vault_build(payload.get("vault_path", ""), payload)
        track_template_version(payload.get("vault_path", ""), payload)
    except Exception as e:
        logger.error(
            f"Audit/monitor/version tracking failed: {e}\n{traceback.format_exc()}"
        )
        errors.append(f"Audit: {e}")
    # Log to vault event log/activity log
    try:
        from autonomy.utils.vault_event_log import log_vault_event
        from autonomy.utils.activity_log import log_activity

        log_vault_event(vault_id, "metadata_updated", payload, errors)
        log_activity(vault_id, "metadata_updated", payload, errors)
    except Exception as e:
        logger.error(f"Vault activity logging failed: {e}\n{traceback.format_exc()}")
    # AI anomaly detection on failures
    try:
        from autonomy.ai_tools.anomaly_detector import detect_anomaly

        if errors:
            detect_anomaly(vault_id, errors)
    except Exception as e:
        logger.error(f"Anomaly detection failed: {e}\n{traceback.format_exc()}")
    # Track build time/performance
    try:
        from autonomy.utils.performance_monitor import monitor_vault_build

        build_time = time.time() - start_time
        monitor_vault_build(
            payload.get("vault_path", ""), {**payload, "build_time": build_time}
        )
    except Exception as e:
        logger.error(f"Performance monitoring failed: {e}\n{traceback.format_exc()}")
    print(f"[AIFOLIO] Metadata updated for vault {vault_id} by user {user_id}.")
    return {"status": "success", "vault_id": vault_id, "errors": errors}
