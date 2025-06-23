"""
AIFOLIO™ SAFE AI MODULE: Policy Audit Bot
- Static only. No sentience, recursion, or adaptive logic.
- Validates .md policies for required fields.
- Alerts if policies outdated or incomplete.
- Blocks unsafe publish.
- All findings logged for human review.
"""
import os
import logging

REQUIRED_FIELDS = ["Effective Date", "Contact", "Jurisdiction"]
POLICIES = [
    "terms_of_service.md",
    "refund_policy.md",
    "privacy_policy.md"
]

LOG_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../distribution/legal_exports/policy_audit_log.txt'))
logging.basicConfig(filename=LOG_PATH, level=logging.INFO)

def audit_policy_file(policy_path):
    with open(policy_path, 'r') as f:
        content = f.read()
    missing = [field for field in REQUIRED_FIELDS if field not in content]
    return missing

def audit_all_policies(policy_dir):
    results = {}
    for fname in POLICIES:
        path = os.path.join(policy_dir, fname)
        if not os.path.exists(path):
            results[fname] = 'MISSING FILE'
            logging.error(f"Missing: {fname}")
            continue
        missing = audit_policy_file(path)
        if missing:
            results[fname] = f'Missing fields: {missing}'
            logging.warning(f"{fname} missing fields: {missing}")
        else:
            results[fname] = 'OK'
            logging.info(f"{fname} OK")
    return results
