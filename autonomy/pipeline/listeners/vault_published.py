from autonomy.product_prep.gumroad_delivery import push_vault_to_gumroad

import os
import time
import logging
import traceback
from autonomy.product_prep.gumroad_delivery import push_vault_to_gumroad
from autonomy.integrations.analytics_reporting import report_to_analytics
from autonomy.ai_tools.anomaly_detector import detect_anomaly
from autonomy.ai_tools.audit_compliance import check_vault_metadata
from autonomy.utils.dashboard_push import push_dashboard_update
from autonomy.utils.slack_alert import send_slack_alert
from autonomy.utils.telegram_alert import send_telegram_alert
from autonomy.utils.email_alert import send_email_alert
from autonomy.utils.vault_event_log import log_vault_event
from autonomy.utils.performance_monitor import monitor_vault_build
from autonomy.utils.version_tracker import track_template_version
from autonomy.utils.retry import retry_safe
from autonomy.utils.activity_log import log_activity

logger = logging.getLogger("vault_published")

@retry_safe(max_attempts=3, backoff_factor=2)
def sync_integrations(metadata):
    push_vault_to_gumroad(metadata.get("metadata_path"), metadata.get("preview_path"), metadata.get("file_path"))
    report_to_analytics(metadata)

@retry_safe(max_attempts=3, backoff_factor=2)
def send_alerts(metadata, event_type, error=None):
    alert_msg = f"Vault {event_type}: {metadata.get('title', 'N/A')} (ID: {metadata.get('vault_id', 'N/A')})"
    if error:
        alert_msg += f"\nError: {error}"
    send_slack_alert(alert_msg)
    send_telegram_alert(alert_msg)
    if metadata.get("alert_email_opt_in"):
        send_email_alert(metadata.get("owner_email"), alert_msg)

@retry_safe(max_attempts=3, backoff_factor=2)
def push_dashboard(vault_id, payload):
    push_dashboard_update(vault_id, payload)

@retry_safe(max_attempts=3, backoff_factor=2)
def audit_and_monitor(metadata):
    audit_vault_compliance(metadata.get("vault_path", ""), metadata)
    monitor_vault_build(metadata.get("vault_path", ""), metadata)
    track_template_version(metadata.get("vault_path", ""), metadata)

def handle_event(metadata):
    """
    Handles the 'vault_published' event with SAFE AI, retry-safe integrations, and robust logging.
    """
    vault_id = metadata.get("vault_id") or metadata.get("title", "").replace(" ", "_").lower()
    start_time = time.time()
    errors = []
    # --- Static AI Compliance & Anomaly Checks ---
    ai_results = {}
    compliance_result = check_vault_metadata(metadata)
    ai_results['compliance'] = compliance_result
    anomaly_flags = []
    if not compliance_result['compliant']:
        anomaly_flags.append('compliance_failure')
    if not metadata.get('preview_path'):
        anomaly_flags.append('missing_preview')
    if not metadata.get('metadata_path'):
        anomaly_flags.append('missing_metadata')
    if not metadata.get('final_validation_passed', True):
        anomaly_flags.append('final_validation_failed')
    ai_results['anomaly_flags'] = anomaly_flags
    # If any anomaly or compliance failure, trigger alerts and outbound webhooks
    if anomaly_flags or not compliance_result['compliant']:
        alert_msg = f"[AI] Vault published anomaly/compliance issue: {anomaly_flags}, {compliance_result}"
        send_slack_alert(alert_msg)
        send_telegram_alert(alert_msg)
        if metadata.get("alert_email_opt_in"):
            send_email_alert(metadata.get("owner_email"), alert_msg)
        # Outbound webhook (future-proof, e.g. Zapier)
        try:
            from autonomy.post_sale_hooks.outbound_webhook import post_outbound_webhooks
            post_outbound_webhooks({"event":"vault_published","metadata":metadata,"ai_results":ai_results})
        except Exception as e:
            logger.warning(f"Outbound webhook failed: {e}")
    # --- End AI Checks ---
    # Gumroad upload and analytics
    try:
        sync_integrations(metadata)
    except Exception as e:
        logger.error(f"Integration sync failed: {e}\n{traceback.format_exc()}")
        errors.append(f"Integration: {e}")
        send_alerts(metadata, "published", error=str(e))
    # Dashboard update
    try:
        push_dashboard(vault_id, metadata)
    except Exception as e:
        logger.error(f"Dashboard update failed: {e}\n{traceback.format_exc()}")
        errors.append(f"Dashboard: {e}")
    # Audit, monitor, version tracking
    try:
        audit_and_monitor(metadata)
    except Exception as e:
        logger.error(f"Audit/monitor/version tracking failed: {e}\n{traceback.format_exc()}")
        errors.append(f"Audit: {e}")
    # Required metadata/previews check
    try:
        assert metadata.get("metadata_path") and metadata.get("preview_path"), "Missing Gumroad metadata or preview"
        assert metadata.get("final_validation_passed", True), "Final validation failed"
    except Exception as e:
        logger.error(f"Final validation failed: {e}\n{traceback.format_exc()}")
        errors.append(f"Validation: {e}")
        send_alerts(metadata, "published", error=str(e))
    # Log to vault event log/activity log (with ai_results)
    try:
        log_vault_event(vault_id, "published", {**metadata, "ai_results": ai_results}, errors)
        log_activity(vault_id, "published", {**metadata, "ai_results": ai_results}, errors)
    except Exception as e:
        logger.error(f"Vault activity logging failed: {e}\n{traceback.format_exc()}")
    # AI anomaly detection on failures
    if errors:
        try:
            detect_anomaly(vault_id, errors)
        except Exception as e:
            logger.error(f"Anomaly detection failed: {e}\n{traceback.format_exc()}")
    # Track build time/performance
    try:
        build_time = time.time() - start_time
        monitor_vault_build(metadata.get("vault_path", ""), {**metadata, "build_time": build_time})
    except Exception as e:
        logger.error(f"Performance monitoring failed: {e}\n{traceback.format_exc()}")
    return {"status": "success", "vault_id": vault_id, "errors": errors}
