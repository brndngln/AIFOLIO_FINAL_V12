"""
AIFOLIO AI Guardrail Layer
Static, deterministic, SAFE AI-compliant guardrail logic for all AI modules.
"""
import logging

logger = logging.getLogger(__name__)

STATIC_GUARDRAILS = [
    "No sentience",
    "No adaptation",
    "Deterministic outputs",
    "OWNER override required for all critical actions",
    "Audit logging for every operation",
    "No cryptographically seeded randomness",
    "No live API calls at runtime",
    "Prompt injection prevention",
    "No dynamic AI tuning",
    "No external AI at runtime",
    "All extension points documented",
]


def get_guardrails() -> list:
    logger.info(f"AI guardrails: {STATIC_GUARDRAILS}")
    return STATIC_GUARDRAILS
