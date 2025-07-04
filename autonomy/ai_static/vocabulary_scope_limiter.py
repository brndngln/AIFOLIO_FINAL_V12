"""
AIFOLIO™ SAFE AI MODULE: Vocabulary Scope Limiter
- Static, non-sentient
- Restricts output vocabulary to pre-approved list
- Logs all restricted outputs
"""
import logging

LOG_PATH = "../../distribution/legal_exports/vocab_limiter_log.txt"
logging.basicConfig(filename=LOG_PATH, level=logging.INFO)

ALLOWED_WORDS = set([
    "purchase", "refund", "vault", "policy", "export", "user", "admin", "success", "failure", "pending"
])

def limit_vocabulary(text):
    words = text.split()
    limited = [w for w in words if w in ALLOWED_WORDS]
    result = ' '.join(limited)
    logging.info(f"Vocabulary limited: {result}")
    return result
