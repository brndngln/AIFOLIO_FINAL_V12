"""
Static, deterministic tone/voice analytics for AIFOLIO™. SAFE AI, owner-controlled, fully auditable.
"""
def check_tone_voice(text, brand_profile):
    """Return static analysis of tone and brand match."""
    if brand_profile.lower() in text.lower():
        return {'match': True, 'tone': 'consistent', 'confidence': 1.0}
    return {'match': False, 'tone': 'inconsistent', 'confidence': 0.7}
