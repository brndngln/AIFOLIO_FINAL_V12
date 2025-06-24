"""
AIFOLIO SAFE AI Visual Balance Checker
Static, deterministic checker for basic visual layout issues.
"""
import logging
logger = logging.getLogger(__name__)

STATIC_ALLOWED_ASPECT_RATIOS = [(1,1), (16,9), (4,3)]

def check_visual_balance(width: int, height: int) -> dict:
    """Static, deterministic visual balance checker. Extension: real image analysis."""
    aspect_ratio = (width, height)
    allowed = aspect_ratio in STATIC_ALLOWED_ASPECT_RATIOS
    result = {
        'aspect_ratio': aspect_ratio,
        'allowed': allowed,
        'requires_human_review': not allowed
    }
    logger.info(f"Checked visual balance for {width}x{height}: {result}")
    return result
