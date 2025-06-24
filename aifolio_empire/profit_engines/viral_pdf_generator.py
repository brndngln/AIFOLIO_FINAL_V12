"""
AIFOLIO Auto Viral PDF Generator
Static, deterministic, SAFE AI-compliant viral title, cover, and CTA generator.
"""
import logging
logger = logging.getLogger(__name__)

STATIC_TITLES = [
    'Unlock the Secret to Tax-Free Wealth!',
    'The Ultimate Guide to Passive Income in 2025',
    'Top 10 Security Mistakes Entrepreneurs Make',
    'How to Build a Personal Brand That Sells'
]
STATIC_COVERS = [
    'golden-vault.png',
    'influencer-blueprint.png',
    'cybersecurity-shield.png'
]
STATIC_CTAS = [
    'Download Now',
    'Get Your Free Copy',
    'Start Winning Today'
]

def generate_viral_pdf_assets() -> dict:
    result = {
        'title': STATIC_TITLES[0],
        'cover': STATIC_COVERS[0],
        'cta': STATIC_CTAS[0]
    }
    logger.info(f"Generated viral PDF assets: {result}")
    return result
