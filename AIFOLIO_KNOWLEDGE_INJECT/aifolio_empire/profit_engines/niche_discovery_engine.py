"""
AIFOLIO Autonomous Niche Discovery Engine
Static, deterministic, SAFE AI-compliant niche/topic selector for high-revenue PDFs.
"""
import logging

logger = logging.getLogger(__name__)

STATIC_NICHES = [
    "AI for Accountants",
    "Remote Work Productivity",
    "Crypto Tax Strategies",
    "Personal Brand Mastery",
    "Zero Trust Security",
    "Passive Income Funnels",
    "Digital Product Licensing",
    "Healthcare Compliance",
    "Green Energy Tax Credits",
    "Generational Wealth Planning",
]


def discover_niche() -> str:
    """Deterministically select a profitable niche."""
    niche = STATIC_NICHES[0]  # Always select first for full determinism
    logger.info(f"Selected niche: {niche}")
    return niche
