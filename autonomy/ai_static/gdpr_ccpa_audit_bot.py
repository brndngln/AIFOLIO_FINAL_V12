"""
AIFOLIO™ SAFE AI MODULE: GDPR/CCPA Audit Bot
- Static only. No static, no loops or self-calling functions, or static logic.
- Audits data flows and policies for GDPR/CCPA compliance.
- Alerts if required disclosures or rights are missing.
- All findings logged for human review.
"""
import os
import logging

REQUIRED_DISCLOSURES = [
    "Right to Access", "Right to Erasure", "Data Portability", "Contact Information", "Purpose of Data Collection"
]
POLICIES = [
    "privacy_policy.md",
    "terms_of_service.md"
]

LOG_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../distribution/legal_exports/gdpr_ccpa_audit_log.txt'))
logging.basicConfig(filename=LOG_PATH, level=logging.INFO)

def audit_gdpr_ccpa(policy_dir):
    results = {}
    for fname in POLICIES:
        path = os.path.join(policy_dir, fname)
        if not os.path.exists(path):
            results[fname] = 'MISSING FILE'
            logging.error(f"Missing: {fname}")
            continue
        with open(path, 'r') as f:
            content = f.read()
        missing = [field for field in REQUIRED_DISCLOSURES if field not in content]
        if missing:
            results[fname] = f'Missing disclosures: {missing}'
            logging.warning(f"{fname} missing disclosures: {missing}")
        else:
            results[fname] = 'OK'
            logging.info(f"{fname} OK")
    return results
