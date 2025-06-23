"""
SAFE AI Static Module: AI Self-Audit Pipeline
- One AI module audits the logs of others for anomalies or violations
- Static, no recursion, no adaptive logic
- Logs all findings for admin review
"""
import logging
from datetime import datetime
import os

LOG_PATH = "../../distribution/legal_exports/ai_self_audit_log.txt"
logging.basicConfig(filename=LOG_PATH, level=logging.INFO)

MODULE_LOGS = [
    "policy_audit_log.txt",
    "gdpr_ccpa_audit_log.txt",
    "refund_optimizer_log.txt",
    "vault_delivery_monitor_log.txt"
]


def audit_ai_logs(triggered_by):
    timestamp = datetime.utcnow().isoformat()
    findings = []
    for log_file in MODULE_LOGS:
        path = os.path.join("../../distribution/legal_exports/", log_file)
        if os.path.exists(path):
            with open(path, "r") as f:
                for line in f:
                    if "ERROR" in line or "VIOLATION" in line or "BLOCKED" in line:
                        finding = f"[{timestamp}] AUDIT: {log_file} | {line.strip()} | Triggered by: {triggered_by}"
                        findings.append(finding)
                        logging.info(finding)
    if not findings:
        logging.info(f"[{timestamp}] AUDIT: No issues found. | Triggered by: {triggered_by}")
    return findings or ["No issues found."]
