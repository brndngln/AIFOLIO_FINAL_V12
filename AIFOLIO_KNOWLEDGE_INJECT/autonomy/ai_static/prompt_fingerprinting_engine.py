"""
AIFOLIO™ SAFE AI MODULE: Prompt Fingerprinting Engine
- Static, non-sentient
- Generates a hash/fingerprint for each AI prompt
- Used for audit trails and anti-tampering
"""
import hashlib
import logging

LOG_PATH = "../../distribution/legal_exports/prompt_fingerprint_log.txt"
logging.basicConfig(filename=LOG_PATH, level=logging.INFO)


def fingerprint_prompt(prompt_text):
    fp = hashlib.sha256(prompt_text.encode("utf-8")).hexdigest()
    logging.info(f"Prompt fingerprint: {fp}")
    return fp
