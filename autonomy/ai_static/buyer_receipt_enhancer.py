"""
AIFOLIO™ SAFE AI MODULE: Buyer Receipt Enhancer
- Static only. No content generation, no sentience, no recursion.
- Adjusts receipt language for tone (SAFE, friendly, professional).
- NO content creation or legal adaptation.
- All changes are logged and require human approval.
"""
import logging

LOG_PATH = "../../distribution/receipts/receipt_enhance_log.txt"
logging.basicConfig(filename=LOG_PATH, level=logging.INFO)

SAFE_TONE_MAP = {
    "Thank you for your purchase.": "Thank you for your purchase! We appreciate your trust in AIFOLIO™.",
    "Contact us for support.": "If you have any questions, our support team is here to help.",
}

def enhance_receipt_text(text):
    """Replace phrases for tone only."""
    for k, v in SAFE_TONE_MAP.items():
        text = text.replace(k, v)
    logging.info(f"Receipt enhanced: {text}")
    return text
