from autonomy.compliance.export_engine import export_to_xbrl, export_to_csv
import os
import json

import time
from autonomy.utils.dashboard_push import push_dashboard_update
from autonomy.utils.slack_alert import send_slack_alert
from autonomy.utils.telegram_alert import send_telegram_alert
from autonomy.utils.email_alert import send_email_alert
from autonomy.utils.vault_event_log import log_vault_event
from autonomy.utils.performance_monitor import monitor_vault_build
from autonomy.utils.version_tracker import track_template_version
from autonomy.utils.activity_log import log_activity
from autonomy.ai_tools.anomaly_detector import detect_anomaly
from autonomy.ai_tools.audit_compliance import check_vault_metadata


def handle_event(payload):
    """
    Handles the 'delivery_sent' event with SAFE AI, retry-safe integrations, and robust logging.
    """
    delivery_log_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../../../analytics/delivery_log.json")
    )
    errors = []
    start_time = time.time()
    # --- Static AI Delivery Anomaly/Compliance Checks ---
    ai_results = {}
    compliance_result = (
        check_vault_metadata(payload)
        if "vault_id" in payload
        else {"compliant": True, "missing": [], "invalid": []}
    )
    ai_results["compliance"] = compliance_result
    anomaly_flags = []
    # Static anomaly detection: repeated delivery, suspicious IP, missing confirmation
    if payload.get("delivery_attempts", 1) > 3:
        anomaly_flags.append("repeated_delivery")
    if payload.get("ip_address", "").startswith("10."):
        anomaly_flags.append("internal_ip_delivery")
    if not payload.get("confirmation", False):
        anomaly_flags.append("missing_confirmation")
    if not compliance_result["compliant"]:
        anomaly_flags.append("compliance_failure")
    ai_results["anomaly_flags"] = anomaly_flags
    # If any anomaly or compliance failure, trigger alerts and outbound webhooks
    if anomaly_flags or not compliance_result["compliant"]:
        alert_msg = f"[AI] Delivery anomaly/compliance issue: {anomaly_flags}, {compliance_result}"
        send_slack_alert(alert_msg)
        send_telegram_alert(alert_msg)
        if payload.get("alert_email_opt_in"):
            send_email_alert(payload.get("owner_email"), alert_msg)
        # Outbound webhook (future-proof, e.g. Zapier)
        try:
            from autonomy.post_sale_hooks.outbound_webhook import post_outbound_webhooks

            post_outbound_webhooks(
                {"event": "delivery_sent", "payload": payload, "ai_results": ai_results}
            )
        except Exception as e:
            print(f"Outbound webhook failed: {e}")
    # --- End AI Checks ---
    entry = {
        "event": "delivery_sent",
        "payload": payload,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "ai_results": ai_results,
    }
    # Log delivery event
    try:
        if os.path.exists(delivery_log_path):
            with open(delivery_log_path, "r+") as f:
                logs = json.load(f)
                logs.append(entry)
                f.seek(0)
                json.dump(logs, f, indent=2)
        else:
            with open(delivery_log_path, "w") as f:
                json.dump([entry], f, indent=2)
    except Exception as e:
        errors.append(f"Log: {e}")
    # XBRL/CSV export
    try:
        if payload.get("export_xbrl"):
            export_to_xbrl(payload)
        if payload.get("export_csv"):
            export_to_csv(payload, f"{payload.get('vault_id', 'unknown')}_delivery.csv")
    except Exception as e:
        errors.append(f"Export: {e}")
    # Dashboard update
    try:
        push_dashboard_update(payload.get("vault_id", "unknown"), payload)
    except Exception as e:
        errors.append(f"Dashboard: {e}")
    # Audit, monitor, version tracking
    try:
        audit_vault_compliance(payload.get("vault_path", ""), payload)
        monitor_vault_build(payload.get("vault_path", ""), payload)
        track_template_version(payload.get("vault_path", ""), payload)
    except Exception as e:
        errors.append(f"Audit: {e}")
    # Alerts
    try:
        msg = f"Vault delivered: {payload.get('vault_id', 'unknown')}"
        send_slack_alert(msg)
        send_telegram_alert(msg)
        if payload.get("alert_email_opt_in"):
            send_email_alert(payload.get("owner_email"), msg)
    except Exception as e:
        errors.append(f"Alert: {e}")
    # Log to vault event log/activity log (with ai_results)
    try:
        log_vault_event(
            payload.get("vault_id", "unknown"),
            "delivery_sent",
            {**payload, "ai_results": ai_results},
            errors,
        )
        log_activity(
            payload.get("vault_id", "unknown"),
            "delivery_sent",
            {**payload, "ai_results": ai_results},
            errors,
        )
    except Exception as e:
        errors.append(f"VaultLog: {e}")
    # AI anomaly detection on failures
    if errors:
        try:
            detect_anomaly(payload.get("vault_id", "unknown"), errors)
        except Exception:
            pass
    # Track build time/performance
    try:
        build_time = time.time() - start_time
        monitor_vault_build(
            payload.get("vault_path", ""), {**payload, "build_time": build_time}
        )
    except Exception:
        pass
    return {
        "status": "success",
        "vault_id": payload.get("vault_id", "unknown"),
        "errors": errors,
    }
