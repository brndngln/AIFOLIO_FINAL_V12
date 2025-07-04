from autonomy.showcase import vault_preview_builder
from autonomy.pricing import pricing_engine
from autonomy.compliance.tax_engine import TaxEngine
from autonomy.compliance.workflow_engine import trigger_compliance_workflow

import time
import logging
import traceback
from autonomy.pricing import price_test_engine
from autonomy.product_prep.gumroad_delivery import push_vault_to_gumroad
from autonomy.integrations.stripe_sync import sync_to_stripe
from autonomy.integrations.notion_sync import sync_to_notion
from autonomy.integrations.crm_sync import sync_to_crm
from autonomy.integrations.analytics_reporting import report_to_analytics
from autonomy.integrations.xbrl_export import export_to_xbrl
from autonomy.ai_tools.vault_formatter import format_title, format_description
from autonomy.ai_tools.anomaly_detector import detect_anomaly
from autonomy.ai_tools.audit_bot import audit_vault_compliance
from autonomy.utils.dashboard_push import push_dashboard_update
from autonomy.utils.slack_alert import send_slack_alert
from autonomy.utils.telegram_alert import send_telegram_alert
from autonomy.utils.email_alert import send_email_alert
from autonomy.utils.performance_monitor import monitor_vault_build
from autonomy.utils.version_tracker import track_template_version
from autonomy.utils.retry import retry_safe

logger = logging.getLogger("vault_created")

# Retry-safe wrapper with exponential backoff
@retry_safe(max_attempts=3, backoff_factor=2)
def trigger_preview(vault_path, metadata):
    vault_preview_builder.build_vault_preview(vault_path, metadata)

@retry_safe(max_attempts=3, backoff_factor=2)
def trigger_pricing(vault_path, metadata):
    pricing_engine.trigger_pricing_on_vault_event(vault_path, metadata)

@retry_safe(max_attempts=3, backoff_factor=2)
def trigger_price_test(vault_path, vault_id, metadata):
    if metadata.get("auto_price_testing", False):
        price_test_engine.trigger_price_test_and_update_metadata(vault_path, vault_id, metadata)

@retry_safe(max_attempts=3, backoff_factor=2)
def sync_integrations(vault_path, metadata):
    push_vault_to_gumroad(metadata.get("metadata_path"), metadata.get("preview_path"), metadata.get("file_path"))
    sync_to_stripe(metadata)
    sync_to_notion(metadata)
    sync_to_crm(metadata)
    report_to_analytics(metadata)
    export_to_xbrl(metadata)

@retry_safe(max_attempts=3, backoff_factor=2)
def send_alerts(metadata, event_type, error=None):
    alert_msg = f"Vault {event_type}: {metadata.get('title')} (ID: {metadata.get('vault_id', 'N/A')})"
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
def audit_and_monitor(vault_path, metadata):
    audit_vault_compliance(vault_path, metadata)
    monitor_vault_build(vault_path, metadata)
    track_template_version(vault_path, metadata)


def handle_event(metadata):
    """
    Handles the 'vault_created' event with SAFE AI logic, full integration, and robust error handling.
    """
    # SAFE AI VALIDATION LAYER (block on failure)
    from autonomy.validation import automation_safeguard
    valid, safeguard_msg = automation_safeguard.enforce_all_safeguards(metadata)
    vault_id = metadata.get("vault_id") or metadata.get("title", "").replace(" ", "_").lower()
    errors = []
    if not valid:
        import logging
        logger = logging.getLogger("vault_created")
        logger.error(f"SAFEGUARD BLOCK: {safeguard_msg}")
        errors.append(f"SAFEGUARD: {safeguard_msg}")
        automation_safeguard.audit_log('SAFEGUARD_BLOCKED', {'vault_id': vault_id, 'reason': safeguard_msg, 'metadata': metadata})
        # Optionally send alert
        try:
            from autonomy.compliance.alert_engine import send_alert
            send_alert(type="safeguard_blocked", message=safeguard_msg, to=metadata.get("owner_email"))
        except Exception:
            pass
        # Log and abort further processing
        from autonomy.utils.vault_event_log import log_vault_event
        from autonomy.utils.activity_log import log_activity
        log_vault_event(vault_id, "safeguard_blocked", metadata, errors)
        log_activity(vault_id, "safeguard_blocked", metadata, errors)
        return {"status": "blocked", "vault_id": vault_id, "errors": errors}
    # Validate vault metadata
    assert "title" in metadata and "niche" in metadata, "Missing vault metadata fields"
    vault_path = metadata.get("vault_path") or f"vaults/{vault_id}"
    start_time = time.time()
    # Static rule-based formatting (grammar/capitalization)
    metadata["title"] = format_title(metadata["title"])
    if "description" in metadata:
        metadata["description"] = format_description(metadata["description"])

    # --- Static AI Compliance & Anomaly Checks ---
    from autonomy.ai_tools.audit_compliance import check_vault_metadata
    ai_results = {}
    compliance_result = check_vault_metadata(metadata)
    ai_results['compliance'] = compliance_result
    # Anomaly detection: outliers, suspicious patterns (static)
    anomaly_flags = []
    if not compliance_result['compliant']:
        anomaly_flags.append('compliance_failure')
    if len(metadata.get('title','')) < 5 or len(metadata.get('description','')) < 10:
        anomaly_flags.append('metadata_too_short')
    ai_results['anomaly_flags'] = anomaly_flags
    # If any anomaly or compliance failure, trigger alerts and outbound webhooks
    if anomaly_flags or not compliance_result['compliant']:
        alert_msg = f"[AI] Vault anomaly/compliance issue: {anomaly_flags}, {compliance_result}"
        send_slack_alert(alert_msg)
        send_telegram_alert(alert_msg)
        if metadata.get("alert_email_opt_in"):
            send_email_alert(metadata.get("owner_email"), alert_msg)
        # Outbound webhook (future-proof, e.g. Zapier)
        try:
            from autonomy.post_sale_hooks.outbound_webhook import post_outbound_webhooks
            post_outbound_webhooks({"event":"vault_created","metadata":metadata,"ai_results":ai_results})
        except Exception as e:
            logger.warning(f"Outbound webhook failed: {e}")
    # --- End AI Checks ---
    # Trigger preview generation
    try:
        trigger_preview(vault_path, metadata)
    except Exception as e:
        logger.error(f"Preview generation failed: {e}\n{traceback.format_exc()}")
        errors.append(f"Preview: {e}")
        send_alerts(metadata, "created", error=str(e))
    # Trigger pricing engine
    try:
        trigger_pricing(vault_path, metadata)
    except Exception as e:
        logger.error(f"Pricing engine failed: {e}\n{traceback.format_exc()}")
        errors.append(f"Pricing: {e}")
        send_alerts(metadata, "created", error=str(e))
    # Trigger price test engine if enabled
    try:
        trigger_price_test(vault_path, vault_id, metadata)
    except Exception as e:
        logger.error(f"Price test engine failed: {e}\n{traceback.format_exc()}")
        errors.append(f"PriceTest: {e}")
        send_alerts(metadata, "created", error=str(e))
    # Integrations (Gumroad, Stripe, Notion, CRM, Analytics, XBRL)
    try:
        sync_integrations(vault_path, metadata)
    except Exception as e:
        logger.error(f"Integration sync failed: {e}\n{traceback.format_exc()}")
        errors.append(f"Integration: {e}")
        send_alerts(metadata, "created", error=str(e))
    # Dashboard update (real-time)
    try:
        push_dashboard(vault_id, metadata)
    except Exception as e:
        logger.error(f"Dashboard update failed: {e}\n{traceback.format_exc()}")
        errors.append(f"Dashboard: {e}")
    # Audit, monitor, version tracking
    try:
        audit_and_monitor(vault_path, metadata)
    except Exception as e:
        logger.error(f"Audit/monitor/version tracking failed: {e}\n{traceback.format_exc()}")
        errors.append(f"Audit: {e}")
    # Compliance workflow
    try:
        trigger_compliance_workflow(event="vault_created", data=metadata)
    except Exception as e:
        logger.error(f"Compliance workflow failed: {e}\n{traceback.format_exc()}")
        errors.append(f"Compliance: {e}")
    # Tax jurisdiction check
    try:
        tax = TaxEngine.get_tax_rate(country_code=metadata.get("country", "US"))
        metadata["tax"] = tax
    except Exception as e:
        logger.error(f"Tax check failed: {e}\n{traceback.format_exc()}")
        errors.append(f"Tax: {e}")
    # Log to vault activity log, including ai_results
    try:
        log_vault_event(vault_id, "created", {**metadata, "ai_results": ai_results}, errors)
        log_activity(vault_id, "created", {**metadata, "ai_results": ai_results}, errors)
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
        monitor_vault_build(vault_path, {**metadata, "build_time": build_time})
    except Exception as e:
        logger.error(f"Performance monitoring failed: {e}\n{traceback.format_exc()}")
    # Always return, never block main vault delivery
    return {"status": "success", "vault_id": vault_id, "errors": errors}
