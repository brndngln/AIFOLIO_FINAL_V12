"""
AIFOLIO PDF Cross-Promotion Engine
Static, deterministic, SAFE AI-compliant cross-linking for PDF products.
"""
import logging
logger = logging.getLogger(__name__)

STATIC_CROSS_LINKS = [
    {'from': 'Tax-Free Wealth', 'to': 'Passive Income 2025'},
    {'from': 'Brand Mastery', 'to': 'Ultimate Profit Bundle'},
    {'from': 'Zero Trust Guide', 'to': 'SIEM Playbook'}
]

def get_cross_promotions(pdf_title: str) -> list:
    links = [link['to'] for link in STATIC_CROSS_LINKS if link['from'] == pdf_title]
    logger.info(f"Cross-promotions for {pdf_title}: {links}")
    return links
