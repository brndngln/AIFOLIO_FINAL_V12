"""
AIFOLIO Multi-Channel PDF Funnel Engine
Static, deterministic, SAFE AI-compliant funnel generator for email, social, blog, affiliate channels.
"""
import logging
logger = logging.getLogger(__name__)

CHANNELS = ['email', 'social', 'blog', 'affiliate']
STATIC_UTM_TAGS = {
    'email': 'utm_source=email&utm_medium=campaign',
    'social': 'utm_source=social&utm_medium=organic',
    'blog': 'utm_source=blog&utm_medium=content',
    'affiliate': 'utm_source=affiliate&utm_medium=partner'
}

STATIC_FUNNEL_TEMPLATES = {
    'email': 'Download your exclusive PDF now! [CTA]',
    'social': 'Unlock your free guide — link in bio!',
    'blog': 'Get the full PDF by subscribing below.',
    'affiliate': 'Special offer PDF for our partner audience!'
}

def generate_funnel(channel: str, pdf_title: str) -> dict:
    """Deterministic funnel generator for a given channel."""
    if channel not in CHANNELS:
        raise ValueError(f"Invalid channel: {channel}")
    funnel = {
        'channel': channel,
        'utm_tag': STATIC_UTM_TAGS[channel],
        'template': STATIC_FUNNEL_TEMPLATES[channel].replace('[CTA]', f'Get {pdf_title} now!')
    }
    logger.info(f"Generated funnel for {channel}: {funnel}")
    return funnel
