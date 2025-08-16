"""SAFE AI MODULE"""

"SAFE AI MODULE"
"SAFE AI MODULE"
from typing import Dict


def monitor_legal_horizon(events: Dict[str, str]) -> bool:
    return any(("expiry" in v or "pending" in v for v in events.values()))
