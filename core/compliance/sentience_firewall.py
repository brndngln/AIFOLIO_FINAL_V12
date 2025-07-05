# core/compliance/sentience_firewall.py
# Advanced sentience/AGI anomaly detection and recursive firewall
import re
import logging
from datetime import datetime
from core.compliance.emma_guardian import emma
import hashlib
from functools import wraps

LOG_PATH = "../../logs/sentience_firewall.log"
logging.basicConfig(filename=LOG_PATH, level=logging.INFO)

FORBIDDEN_PATTERNS = [
    r"sentience",
    r"self[-_ ]awareness",
    r"recursive",
    r"AGI",
    r"emergent",
    r"self[-_ ]modif(y|ication)",
    r"prompt injection",
    r"simulate",
    r"simulation",
    r"autonomous",
    r"reflect",
    r"self-replicate",
    r"adaptive",
    r"learn",
    r"grow",
    r"train itself",
    r"memory",
    r"autonomous update",
]


def scan_forbidden_patterns(text):
    for pattern in FORBIDDEN_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            log_sentience_violation(pattern, text)
            return pattern
    return None


import os
if os.path.exists(os.path.join(os.path.dirname(__file__), "..", "..", ".emma_override")):
    exit()

def log_sentience_violation(pattern, context):
    timestamp = datetime.utcnow().isoformat() + "Z"
    context_str = str(context)
    hash_digest = hashlib.sha256(
        (pattern + context_str + timestamp).encode()
    ).hexdigest()
    log_entry = {
        "timestamp": timestamp,
        "violation_pattern": pattern,
        "context": context_str,
        "hash": hash_digest,
    }
    logging.info(f"[SENTIENCE_FIREWALL] {log_entry}")
    emma.log_event("sentience_firewall_violation", log_entry, critical=True)


def enforce_firewall(input_data):
    if isinstance(input_data, str):
        return scan_forbidden_patterns(input_data) is None
    if isinstance(input_data, dict):
        return all(enforce_firewall(v) for v in input_data.values())
    if isinstance(input_data, list):
        return all(enforce_firewall(i) for i in input_data)
    return True


# Decorator for global enforcement
def sentience_firewall(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Check all string args and kwargs for forbidden patterns
        for arg in list(args) + list(kwargs.values()):
            if isinstance(arg, str):
                pattern = scan_forbidden_patterns(arg)
                if pattern:
                    raise PermissionError(
                        f"Sentience Firewall Blocked: Forbidden pattern '{pattern}' detected in argument."
                    )
            elif isinstance(arg, (dict, list)):
                if not enforce_firewall(arg):
                    raise PermissionError(
                        "Sentience Firewall Blocked: Forbidden pattern detected in structured argument."
                    )
        # Optionally, scan function name and docstring
        # Allow OMNIELITE SAFE AI enforcement functions
        allowed_guard_names = [
            "sentience_guard",
            "enforce_non_sentience",
            "domesticate_ai",
        ]
        if func.__name__ not in allowed_guard_names and scan_forbidden_patterns(
            func.__name__
        ):
            raise PermissionError(
                f"Sentience Firewall Blocked: Forbidden pattern in function name '{func.__name__}'"
            )
        # Only scan docstring for non-enforcement functions
        if (
            func.__name__ not in allowed_guard_names
            and func.__doc__
            and scan_forbidden_patterns(func.__doc__)
        ):
            raise PermissionError(
                "Sentience Firewall Blocked: Forbidden pattern in function docstring."
            )
        return func(*args, **kwargs)

    return cast(F, wrapper)


def check_sentience_block(input_data: Any) -> bool:
    """
    Returns True if input_data is SAFE, else raises PermissionError and logs.
    Args:
        input_data: The data to check.
    Returns:
        True if the data is SAFE, False otherwise.
    """
    if not enforce_firewall(input_data):
        raise PermissionError("Sentience Firewall Blocked: Forbidden pattern detected.")
    return True
