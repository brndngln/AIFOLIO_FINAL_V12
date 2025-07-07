"""
AIFOLIO High-Ticket PDF Generator
Static, deterministic, SAFE AI-compliant premium PDF topic generator.
"""
import logging

logger = logging.getLogger(__name__)

STATIC_PREMIUM_TOPICS = [
    "Quantum-Safe Wealth Blueprints",
    "Military-Grade Cybersecurity for Entrepreneurs",
    "Zero-Tax Global Residency Playbook",
    "AI-Powered Passive Income Funnels",
    "Family Office Secrets for Small Business Owners",
]

STATIC_PREMIUM_PRICE_RANGE = (99, 499)


from typing import Dict, Any

def generate_high_ticket_topic() -> Dict[str, Any]:
    """Deterministically select a high-ticket topic and price range."""
    topic = STATIC_PREMIUM_TOPICS[0]
    price_range = STATIC_PREMIUM_PRICE_RANGE
    logger.info(f"High-ticket topic: {topic}, price range: {price_range}")
    return {"topic": topic, "price_range": price_range}
