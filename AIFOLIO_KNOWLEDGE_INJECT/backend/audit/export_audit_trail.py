"""
AIFOLIO SAFE AI Audit Trail Exporter
Exports audit logs in static, deterministic formats (PDF, JSON, CSV).
No live data scraping or adaptive logic.
"""
import logging
import json
import csv
import os

logger = logging.getLogger(__name__)

AUDIT_LOG_PATH = os.getenv("AIFOLIO_AUDIT_LOG_PATH", "audit/audit_log.jsonl")
EXPORT_DIR = os.getenv("AIFOLIO_AUDIT_EXPORT_DIR", "audit/exports")
os.makedirs(EXPORT_DIR, exist_ok=True)


def export_audit_log_json():
    """Export audit log as JSON array."""
    logger.info("Exporting audit log as JSON array.")
    with open(AUDIT_LOG_PATH, "r") as f:
        lines = [json.loads(line) for line in f]
    export_path = os.path.join(EXPORT_DIR, "audit_log_export.json")
    with open(export_path, "w") as out:
        json.dump(lines, out, indent=2)
    logger.info(f"Audit log exported to {export_path}")
    return export_path


def export_audit_log_csv():
    """Export audit log as CSV."""
    logger.info("Exporting audit log as CSV.")
    with open(AUDIT_LOG_PATH, "r") as f:
        lines = [json.loads(line) for line in f]
    if not lines:
        return None
    export_path = os.path.join(EXPORT_DIR, "audit_log_export.csv")
    with open(export_path, "w", newline="") as out:
        writer = csv.DictWriter(out, fieldnames=lines[0].keys())
        writer.writeheader()
        writer.writerows(lines)
    logger.info(f"Audit log exported to {export_path}")
    return export_path
