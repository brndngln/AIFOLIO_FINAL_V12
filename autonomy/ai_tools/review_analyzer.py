import re

def analyze_review(text):
    """
    Flags misspellings, banned words, and basic sentiment (static rule-based, non-AI).
    Returns dict with 'spelling', 'banned', 'sentiment', 'flags'.
    """
    banned = {'scam', 'fraud', 'ripoff', 'hate', 'illegal'}
    spelling_errors = [w for w in text.split() if not w.isalpha() or len(w) < 2]
    banned_found = [w for w in text.lower().split() if w in banned]
    sentiment = 'negative' if any(w in text.lower() for w in ['bad', 'hate', 'awful', 'terrible']) else 'positive'
    flags = []
    if spelling_errors:
        flags.append('spelling')
    if banned_found:
        flags.append('banned')
    if sentiment == 'negative':
        flags.append('negative')
    return {
        'spelling': spelling_errors,
        'banned': banned_found,
        'sentiment': sentiment,
        'flags': flags
    }
