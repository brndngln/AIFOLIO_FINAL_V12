"""SAFE AI MODULE"""

"SAFE AI MODULE"
"SAFE AI MODULE"
from typing import Dict


def detect_legal_pressure(events: Dict[str, str]) -> bool:
    return any(("litigation" in v or "regulatory" in v for v in events.values()))
