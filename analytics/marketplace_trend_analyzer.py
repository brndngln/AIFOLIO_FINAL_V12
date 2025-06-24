"""
AIFOLIO SAFE AI Marketplace Trend Analyzer
Static, deterministic dashboard for marketplace trends.
"""
import logging
logger = logging.getLogger(__name__)

STATIC_TRENDS = [
    {'category': 'AI Tools', 'trend': 'rising'},
    {'category': 'Legal Templates', 'trend': 'stable'},
    {'category': 'Fitness', 'trend': 'falling'}
]

def get_static_marketplace_trends() -> list:
    """Static, deterministic marketplace trends. Extension: real analytics pipeline."""
    logger.info("Returning static marketplace trends.")
    return STATIC_TRENDS
