"""
AIFOLIO SAFE AI Tone/Voice Matcher
Static, deterministic checker for vault copy tone/voice compliance.
"""
import logging
logger = logging.getLogger(__name__)

STATIC_ALLOWED_TONES = ["premium", "minimalistic", "practical"]

def check_tone_voice(text: str) -> list:
    """Static, deterministic tone/voice matcher. Extension: real NLP pipeline."""
    issues = []
    for tone in STATIC_ALLOWED_TONES:
        if tone not in text.lower():
            issues.append({
                'missing_tone': tone,
                'requires_human_review': True
            })
    logger.info(f"Checked text for tone/voice. Issues: {issues}")
    return issues
