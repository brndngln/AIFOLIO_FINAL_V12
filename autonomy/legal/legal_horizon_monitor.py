"""
Automated Legal Horizon Monitoring — Phase 10+
SAFE, Static Only
"""
from typing import Dict


def monitor_legal_horizon(events: Dict[str, str]) -> bool:
    """Flag legal horizon risks (static, SAFE AI only)"""
    return any("expiry" in v or "pending" in v for v in events.values())
