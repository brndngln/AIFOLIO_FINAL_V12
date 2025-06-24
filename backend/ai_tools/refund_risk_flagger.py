"""
AIFOLIO SAFE AI Refund-Risk Early Warning System
Static, deterministic refund risk flagger. No learning or adaptation.
"""
import logging
logger = logging.getLogger(__name__)

STATIC_HIGH_RISK_REGIONS = ["RegionX", "RegionY"]
STATIC_REPEAT_REFUND_USERS = ["user_123", "user_456"]

def flag_refund_risk(user_id: str, region: str, refund_count: int) -> list:
    """Static, deterministic refund risk flagger. Extension: real risk analytics."""
    flags = []
    if region in STATIC_HIGH_RISK_REGIONS:
        flags.append("high_risk_region")
    if user_id in STATIC_REPEAT_REFUND_USERS or refund_count > 2:
        flags.append("repeat_refunder")
    logger.info(f"Refund risk flags for user {user_id}, region {region}, count {refund_count}: {flags}")
    return flags
