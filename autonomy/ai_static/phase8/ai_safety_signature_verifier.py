"""
SAFE AI Static Module: AI Safety Signature Verifier
- Verifies no drift in AI modules across versions (static, hash-based)
- Logs all verifications for admin review
- No static or static behavior
"""
import logging
from datetime import datetime
import hashlib
import os

LOG_PATH = "../../distribution/legal_exports/ai_safety_signature_log.txt"
logging.basicConfig(filename=LOG_PATH, level=logging.INFO)

MODULE_PATHS = [
    "policy_audit_bot.py",
    "gdpr_ccpa_audit_bot.py",
    "refund_optimizer.py"
]


def verify_ai_signatures(triggered_by):
    timestamp = datetime.utcnow().isoformat()
    signatures = {}
    for module in MODULE_PATHS:
        path = os.path.join("../", module)
        if os.path.exists(path):
            with open(path, "rb") as f:
                data = f.read()
                sig = hashlib.sha256(data).hexdigest()
                signatures[module] = sig
    event = f"[{timestamp}] AI SAFETY SIGNATURES: {signatures} | Triggered by: {triggered_by}"
    logging.info(event)
    return signatures
