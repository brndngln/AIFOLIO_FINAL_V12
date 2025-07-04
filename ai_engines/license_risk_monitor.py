"""
License & Risk Monitor AI (Non-sentient, stateless)
"""
from .sentience_guard import sentience_guard
<<<<<<< HEAD
from core.compliance.threat_feed_parser import parse_threat_feed
from core.compliance.blockchain_license_anchor import anchor_license_hash
from core.compliance.zero_knowledge_export_filter import zero_knowledge_export
from core.compliance.redundant_backup_scheduler import schedule_backup
from core.compliance.compliance_manifest_exporter import export_compliance_manifest
from core.compliance.adaptive_monetization_signal_detector import detect_signals
=======
>>>>>>> omni_repair_backup_20250704_1335
import logging

REGULATED_CATEGORIES = ["finance", "health", "ai", "legal", "medical"]
GDPR_TOPICS = ["personal data", "user data", "privacy"]

@sentience_guard
def legal_scan(product_text, category, user_consent=False):
    # --- OMNIBLADE LEGAL SHIELD: License Risk Audit ---
<<<<<<< HEAD
    import logging, datetime
=======
    import datetime
>>>>>>> omni_repair_backup_20250704_1335
    from core.compliance.smart_legal_watcher import weekly_report
    weekly_report()
    logging.info(f"[LICENSE RISK AUDIT] {datetime.datetime.now().isoformat()} | Asset: {product_text}")
    """
    Scan for missing disclaimers, risky promises, regulated topics.
    Injects legal footer if needed. Checks for explicit consent. Enforces non-sentience and audit logging.
    """
    if category in REGULATED_CATEGORIES:
        product_text += "\n\n[Legal Disclaimer: For informational purposes only. Not financial, legal, or medical advice.]"
        if not user_consent:
            logging.warning("User consent missing for regulated category. Flagging for manual review.")
            product_text += "\n\nFLAG: User consent missing. Manual review required."
    for topic in GDPR_TOPICS:
        if topic in product_text.lower():
            product_text += "\n\n[GDPR Notice: This product may process personal data. Ensure compliance with privacy regulations.]"
    return product_text
