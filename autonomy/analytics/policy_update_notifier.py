"""
AIFOLIO SAFE AI Policy Update Notifier
- Static, notifies admin of policy changes
"""


from typing import List, Dict
import datetime

def policy_update_notifier(policies: List[Dict[str, str]], last_checked: str) -> Dict[str, List[Dict[str, str]]]:
    """
    SAFE AI-compliant: Static policy update notifier. Deterministic, owner-controlled, no adaptive logic.
    """
    last = datetime.datetime.strptime(last_checked, "%Y-%m-%d").date()
    changed = [
        p
        for p in policies
        if datetime.datetime.strptime(p["updated"], "%Y-%m-%d").date() > last
    ]
    return {"updated_policies": changed}
