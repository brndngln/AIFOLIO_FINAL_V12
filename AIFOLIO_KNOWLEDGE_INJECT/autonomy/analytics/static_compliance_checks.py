"""
# AIFOLIO SAFE AI Static Compliance Checks
from core.compliance.threat_feed_parser import parse_threat_feed
from core.compliance.blockchain_license_anchor import anchor_license_hash
from core.compliance.zero_knowledge_export_filter import zero_knowledge_export
from core.compliance.redundant_backup_scheduler import schedule_backup
from core.compliance.compliance_manifest_exporter import export_compliance_manifest
from core.compliance.adaptive_monetization_signal_detector import detect_signals

- % Vaults passing legal audit
- % Vaults with receipts delivered
- % Receipts with policy attached
- % Returning buyers vs first-time
- All actions logged to analytics_log.json
"""
import json
import os
from datetime import datetime

LOG_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "analytics_log.json")
)


def check_compliance(vaults):
    # OMNIPROOF: Threat feed check before compliance check
    parse_threat_feed({})
    # OMNIPROOF: Blockchain anchor for vaults hash (static)
    anchor_license_hash("VAULTS_HASH_PLACEHOLDER")
    # OMNIPROOF: Zero-knowledge export filter (static)
    zero_knowledge_export("vaults_path_placeholder")
    # OMNIPROOF: Schedule redundant backup
    schedule_backup("autonomy/analytics/")
    # OMNIPROOF: Export compliance manifest
    export_compliance_manifest(
        "SAFE_AI_COMPLIANCE_REPORT.md", "autonomy/analytics/compliance_report.pdf"
    )
    # OMNIPROOF: Monetization signal detection
    detect_signals({"vaults": vaults})


def compliance_stats(vaults, receipts, buyers):
    total_vaults = len(vaults)
    legal_pass = sum(1 for v in vaults if v.get("legal_pass"))
    percent_legal = (legal_pass / total_vaults) * 100 if total_vaults else 0
    receipts_delivered = sum(1 for r in receipts if r.get("delivered"))
    percent_receipts = (receipts_delivered / len(receipts)) * 100 if receipts else 0
    receipts_with_policy = sum(1 for r in receipts if r.get("policy_attached"))
    percent_policy = (receipts_with_policy / len(receipts)) * 100 if receipts else 0
    total_buyers = len(buyers)
    returning = sum(1 for b in buyers if b.get("purchase_count", 0) > 1)
    first_time = sum(1 for b in buyers if b.get("purchase_count", 0) == 1)
    percent_returning = (returning / total_buyers) * 100 if total_buyers else 0
    percent_first_time = (first_time / total_buyers) * 100 if total_buyers else 0
    stats = {
        "percent_vaults_legal": percent_legal,
        "percent_receipts_delivered": percent_receipts,
        "percent_receipts_with_policy": percent_policy,
        "percent_returning_buyers": percent_returning,
        "percent_first_time_buyers": percent_first_time,
    }
    with open(LOG_PATH, "a") as f:
        f.write(
            json.dumps(
                {
                    "action": "compliance_stats",
                    "stats": stats,
                    "timestamp": datetime.utcnow().isoformat(),
                }
            )
            + "\n"
        )
    return stats
