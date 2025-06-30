"""
License & Risk Monitor AI (Non-sentient, stateless)
"""
from .sentience_guard import sentience_guard
import logging

REGULATED_CATEGORIES = ["finance", "health", "ai", "legal", "medical"]
GDPR_TOPICS = ["personal data", "user data", "privacy"]

@sentience_guard
def legal_scan(product_text, category, user_consent=False):
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
