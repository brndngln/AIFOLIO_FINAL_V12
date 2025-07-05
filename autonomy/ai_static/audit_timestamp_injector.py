"""
AIFOLIO™ SAFE AI MODULE: Audit Timestamp Injector
- Static, non-sentient
- Injects UTC timestamp into AI outputs for audit trail
"""
from datetime import datetime


def inject_timestamp(output):
    return f"[{datetime.utcnow().isoformat()}] {output}"
