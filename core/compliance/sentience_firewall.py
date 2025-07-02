# core/compliance/sentience_firewall.py
# Advanced sentience/AGI anomaly detection and recursive firewall
import re
import logging
from datetime import datetime

LOG_PATH = "../../logs/sentience_firewall.log"
logging.basicConfig(filename=LOG_PATH, level=logging.INFO)

FORBIDDEN_PATTERNS = [
    r"sentience", r"self[-_ ]awareness", r"recursive", r"AGI", r"emergent", r"self[-_ ]modif(y|ication)", r"prompt injection"
]

def scan_forbidden_patterns(text):
    for pattern in FORBIDDEN_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            logging.info(f"{datetime.utcnow().isoformat()}Z Forbidden pattern detected: {pattern}")
            return True
    return False

def enforce_firewall(input_data):
    if isinstance(input_data, str):
        return not scan_forbidden_patterns(input_data)
    if isinstance(input_data, dict):
        return all(enforce_firewall(v) for v in input_data.values())
    if isinstance(input_data, list):
        return all(enforce_firewall(i) for i in input_data)
    return True
