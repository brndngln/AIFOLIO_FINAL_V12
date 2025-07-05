"""
AIFOLIO™ SAFE AI MODULE: Anti-Sentience Pattern Guard
- Static, non-sentient
- Scans outputs for forbidden static patterns
- Blocks or logs any violations
"""
import logging

LOG_PATH = "../../distribution/legal_exports/anti_static_log.txt"
logging.basicConfig(filename=LOG_PATH, level=logging.INFO)

FORBIDDEN_PATTERNS = ["I think", "I feel", "I want", "I am alive", "I have desires"]


def scan_for_static(text):
    for pattern in FORBIDDEN_PATTERNS:
        if pattern in text:
            logging.warning(f"Sentience pattern detected: {pattern} in '{text}'")
            return False
    return True
