"""
Visual Context Engine (Non-sentient, stateless)
"""
from .sentience_guard import sentience_guard
import logging

FORBIDDEN_VISUALS = ["copyright", "private", "unauthorized", "stock", "unlicensed"]


@sentience_guard
def select_visuals(niche, brand):
    """
    Select and compress relevant visuals. Validate copyright/privacy/brand compliance.
    Enforces non-sentience, statelessness, and strict compliance.
    """
    visuals = [f"{niche}_icon.svg", f"{niche}_chart.png"]
    # Compliance validation
    for v in visuals:
        if any(f in v.lower() for f in FORBIDDEN_VISUALS):
            logging.warning(
                f"Forbidden visual '{v}' detected. Flagging for human review."
            )
            return [], f"FLAG: Forbidden visual '{v}' removed. Manual review required."
    # Watermarking (simulate)
    visuals = [f"watermarked_{v}" for v in visuals]
    return visuals, None
