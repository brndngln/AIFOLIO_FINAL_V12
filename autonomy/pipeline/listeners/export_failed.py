from autonomy.compliance.alert_engine import send_alert
from autonomy.compliance.workflow_engine import trigger_compliance_workflow
import os
import json

import os
import json
import time
import logging
import traceback
from autonomy.compliance.alert_engine import send_alert
from autonomy.compliance.workflow_engine import trigger_compliance_workflow
from autonomy.utils.dashboard_push import push_dashboard_update
from autonomy.utils.slack_alert import send_slack_alert
from autonomy.utils.telegram_alert import send_telegram_alert
from autonomy.utils.email_alert import send_email_alert
from autonomy.utils.vault_event_log import log_vault_event
from autonomy.utils.activity_log import log_activity
from autonomy.ai_tools.anomaly_detector import detect_anomaly
from autonomy.ai_tools.audit_compliance import check_vault_metadata

def handle_event(payload):
    """
    Handles the 'export_failed' event with SAFE AI, retry-safe integrations, and robust logging.
    """
    log_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../analytics/error_log.json'))
    errors = []
    # --- Static AI Root-Cause/Anomaly/Compliance Checks ---
    ai_results = {}
    # Compliance check on payload (if relevant)
    compliance_result = check_vault_metadata(payload) if 'vault_id' in payload else {'compliant': True, 'missing': [], 'invalid': []}
    ai_results['compliance'] = compliance_result
    # Root cause suggestion (static pattern matching)
    anomaly_flags = []
    root_cause = None
    reason = payload.get('reason','').lower()
    if 'timeout' in reason:
        anomaly_flags.append('export_timeout')
        root_cause = 'Export operation timed out.'
    if 'disk' in reason or 'space' in reason:
        anomaly_flags.append('disk_issue')
        root_cause = 'Disk space or IO error.'
    if 'permission' in reason:
        anomaly_flags.append('permission_error')
        root_cause = 'File permission error.'
    if not compliance_result['compliant']:
        anomaly_flags.append('compliance_failure')
    ai_results['anomaly_flags'] = anomaly_flags
    ai_results['root_cause'] = root_cause
    # If any anomaly or compliance failure, trigger alerts and outbound webhooks
    if anomaly_flags or not compliance_result['compliant']:
        alert_msg = f"[AI] Export failed anomaly/compliance/root-cause: {anomaly_flags}, {compliance_result}, {root_cause}"
        send_slack_alert(alert_msg)
        send_telegram_alert(alert_msg)
        if payload.get("alert_email_opt_in"):
            send_email_alert(payload.get("owner_email"), alert_msg)
        # Outbound webhook (future-proof, e.g. Zapier)
        try:
            from autonomy.post_sale_hooks.outbound_webhook import post_outbound_webhooks
            post_outbound_webhooks({"event":"export_failed","payload":payload,"ai_results":ai_results})
        except Exception as e:
            print(f"Outbound webhook failed: {e}")
    # --- End AI Checks ---
    entry = {"event": "export_failed", "payload": payload, "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"), "ai_results": ai_results}
    # --- SAFE FILENAME SANITIZATION & ERROR NOTIFICATION (if applicable) ---
    from autonomy.vaults.filename_sanitizer import enforce_safe_filename
    from autonomy.notifications.email_engine import send_vault_email
    try:
        if payload.get('error_report_path'):
            safe_path = enforce_safe_filename(payload['error_report_path'], payload.get('vault_title', payload.get('vault_id', 'export_error')))
            if payload.get('notify_on_export_error'):
                email_subject = f"[AIFOLIO] Export Error for Vault {payload.get('vault_id', '')}"
                email_body = "An export error occurred. See attached error report."
                send_status = send_vault_email(
                    payload.get('owner_email'),
                    email_subject,
                    email_body,
                    [safe_path]
                )
    except Exception as e:
        errors.append(f"Notify: {e}")
    # Log error event
    try:
        if os.path.exists(log_path):
            with open(log_path, "r+") as f:
                logs = json.load(f)
                logs.append(entry)
                f.seek(0)
                json.dump(logs, f, indent=2)
        else:
            with open(log_path, "w") as f:
                json.dump([entry], f, indent=2)
    except Exception as e:
        errors.append(f"Log: {e}")
    # Alerts
    try:
        msg = f"Export failed: {payload}"
        send_alert(type="export_failed", method="slack", message=msg)
        send_alert(type="export_failed", method="discord", message=msg)
        send_alert(type="export_failed", method="sms", message=msg)
        send_slack_alert(msg)
        send_telegram_alert(msg)
        if payload.get("alert_email_opt_in"):
            send_email_alert(payload.get("owner_email"), msg)
    except Exception as e:
        errors.append(f"Alert: {e}")
    # Dashboard update
    try:
        push_dashboard_update(payload.get("vault_id", "unknown"), payload)
    except Exception as e:
        errors.append(f"Dashboard: {e}")
    # Audit
    try:
        audit_vault_compliance(payload.get("vault_path", ""), payload)
    except Exception as e:
        errors.append(f"Audit: {e}")
    # Log to vault event log/activity log (with ai_results)
    try:
        log_vault_event(payload.get("vault_id", "unknown"), "export_failed", {**payload, "ai_results": ai_results}, errors)
        log_activity(payload.get("vault_id", "unknown"), "export_failed", {**payload, "ai_results": ai_results}, errors)
    except Exception as e:
        errors.append(f"VaultLog: {e}")
    # --- Event Replay/Auto-Remediation Stub ---
    # (Future: implement replay or auto-remediation logic based on root_cause)
    if root_cause:
        print(f"[AIFOLIO][REMEDIATION] Suggested action for export_failed: {root_cause}")
    # AI anomaly detection on failures
    if errors:
        try:
            detect_anomaly(payload.get("vault_id", "unknown"), errors)
        except Exception as e:
            pass
    return {"status": "success", "vault_id": payload.get("vault_id", "unknown"), "errors": errors}
