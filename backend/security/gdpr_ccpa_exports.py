"""
AIFOLIO GDPR/CCPA Safe Exports
Static, deterministic, SAFE AI-compliant export logic for personal data requests.
"""
import logging
import json
logger = logging.getLogger(__name__)

EXPORT_PATH = 'audit/exports/gdpr_ccpa_export.json'

STATIC_EXPORT_FIELDS = [
    'user_id', 'email', 'purchase_history', 'audit_trail', 'compliance_checks'
]

def export_user_data(user: dict) -> str:
    export = {k: user[k] for k in STATIC_EXPORT_FIELDS if k in user}
    with open(EXPORT_PATH, 'w') as f:
        json.dump(export, f, indent=2)
    logger.info(f"Exported GDPR/CCPA data for user {user.get('user_id')}")
    return EXPORT_PATH
