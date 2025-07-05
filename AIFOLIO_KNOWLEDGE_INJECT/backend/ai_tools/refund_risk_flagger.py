"""
AIFOLIO SAFE AI Refund-Risk Early Warning System
Static, deterministic refund risk flagger. No learning or adaptation.
"""
import logging

logger = logging.getLogger(__name__)

STATIC_HIGH_RISK_REGIONS = ["RegionX", "RegionY"]
STATIC_REPEAT_REFUND_USERS = ["user_123", "user_456"]


def flag_refund_risk(user_id: str, region: str, refund_count: int) -> dict:
    """
    Static, deterministic SAFE AI refund risk flagger.
    Returns dict with flags, explanation, recommendation, priority, SAFE AI/owner/non-sentient/version metadata, and audit log.
    All logic is static, deterministic, non-sentient, and owner-controlled.
    """
    VERSION = "AIFOLIO_REFUND_RISK_FLAGGER_V2_SAFEAI_FINAL"
    SAFE_AI_COMPLIANT = True
    OWNER_CONTROLLED = True
    NON_SENTIENT = True
    flags = []
    if region in STATIC_HIGH_RISK_REGIONS:
        flags.append("high_risk_region")
    if user_id in STATIC_REPEAT_REFUND_USERS or refund_count > 2:
        flags.append("repeat_refunder")
    explanation = (
        f"Flags assigned: {flags}" if flags else "No refund risk flags assigned."
    )
    recommendation = "Review user history and region for refund risk."
    priority = 10 if flags else 1
    entry = {
        "timestamp": __import__("datetime").datetime.utcnow().isoformat() + "Z",
        "user_id": user_id,
        "region": region,
        "refund_count": refund_count,
        "flags": flags,
        "explanation": explanation,
        "recommendation": recommendation,
        "priority": priority,
        "version": VERSION,
        "SAFE_AI_COMPLIANT": SAFE_AI_COMPLIANT,
        "OWNER_CONTROLLED": OWNER_CONTROLLED,
        "NON_SENTIENT": NON_SENTIENT,
    }
    logger.info(f"Refund risk audit log: {entry}")
    return entry


# --- Static Drift/Hallucination Protection (stub) ---
def refund_drift_protection():
    return {"drift": False, "explanation": "No drift detected."}


# --- Static Feedback Loop (stub, not user learned) ---
def refund_static_feedback():
    return ["Review flagged users and regions for manual audit."]


# --- Extension Point: Add future static SAFE AI features here ---
