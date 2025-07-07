"""
AIFOLIO™ Gumroad ROI Sync Layer
Real-time funnel logs and A/B test logic. SAFE AI: static, deterministic, owner-controlled.
"""
import logging

STATIC_AB_GROUPS = ["A", "B"]
STATIC_LOGS = []


from typing import Dict

def log_funnel_event(pdf_id: str, event: str, group: str) -> Dict[str, str]:
    if group not in STATIC_AB_GROUPS:
        group = "A"
    entry = {"pdf_id": pdf_id, "event": event, "group": group}
    STATIC_LOGS.append(entry)
    logging.info(f"Gumroad ROI Sync: {entry}")
    return entry
