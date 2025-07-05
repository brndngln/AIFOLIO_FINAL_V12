import logging
from autonomy.utils.slack_alert import send_slack_alert
from autonomy.utils.telegram_alert import send_telegram_alert
from autonomy.utils.email_alert import send_email_alert
from autonomy.utils.vault_event_log import log_vault_event
from autonomy.ai_tools.anomaly_detector import detect_anomaly
from autonomy.ai_tools.audit_compliance import check_vault_metadata


def handle_event(payload):
    """
    Handles the 'policy_violated' event with static AI compliance/anomaly checks and robust logging.
    """
    logger = logging.getLogger("policy_violated")
    errors = []
    ai_results = {}
    compliance_result = (
        check_vault_metadata(payload)
        if "vault_id" in payload
        else {"compliant": True, "missing": [], "invalid": []}
    )
    ai_results["compliance"] = compliance_result
    anomaly_flags = []
    if not compliance_result["compliant"]:
        anomaly_flags.append("compliance_failure")
    if not payload.get("policy_name"):
        anomaly_flags.append("missing_policy_name")
    ai_results["anomaly_flags"] = anomaly_flags
    if anomaly_flags or not compliance_result["compliant"]:
        alert_msg = f"[AI] Policy violation anomaly/compliance: {anomaly_flags}, {compliance_result}"
        send_slack_alert(alert_msg)
        send_telegram_alert(alert_msg)
        if payload.get("alert_email_opt_in"):
            send_email_alert(payload.get("owner_email"), alert_msg)
    try:
        log_vault_event(
            payload.get("vault_id", "unknown"),
            "policy_violated",
            {**payload, "ai_results": ai_results},
            errors,
        )
    except Exception as e:
        logger.error(f"Vault event logging failed: {e}")
    if errors:
        try:
            detect_anomaly(payload.get("vault_id", "unknown"), errors)
        except Exception:
            pass
