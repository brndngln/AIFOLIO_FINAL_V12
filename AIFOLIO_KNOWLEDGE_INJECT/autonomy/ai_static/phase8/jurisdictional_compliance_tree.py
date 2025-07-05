"""
SAFE AI Static Module: Multi-Layer Jurisdictional Compliance Tree
- Maps compliance requirements per region/jurisdiction (static, table-driven)
- Logs all compliance tree generations for audit
- No dynamic, learning, or autonomous behavior (static, table-driven only)
"""
import logging
from datetime import datetime

LOG_PATH = "../../distribution/legal_exports/compliance_tree_log.txt"
logging.basicConfig(filename=LOG_PATH, level=logging.INFO)

COMPLIANCE_TREE = {
    "us": ["GDPR", "CCPA", "SOX"],
    "eu": ["GDPR", "ePrivacy"],
    "apac": ["PDPA", "APPI"],
}


def get_compliance_tree(region, triggered_by):
    timestamp = datetime.utcnow().isoformat()
    requirements = COMPLIANCE_TREE.get(region, [])
    event = f"[{timestamp}] COMPLIANCE TREE: {region} = {requirements} | Triggered by: {triggered_by}"
    logging.info(event)
    return requirements
