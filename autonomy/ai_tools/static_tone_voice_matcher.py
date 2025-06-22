import json
import datetime
import os
import re

TONE_LOG = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../analytics/static_tone_voice_matcher_log.jsonl'))
os.makedirs(os.path.dirname(TONE_LOG), exist_ok=True)

BRAND_TONES = [
    'friendly',
    'professional',
    'enthusiastic',
    'concise',
    'inspiring',
]

# --- AI Static Tone & Voice Matcher (One-Time, Static, Non-Learning) ---
def match_tone(text, target_tone='friendly'):
    # Simple static scorer: checks for exclamation marks, 1st/2nd person, length, etc.
    score = 0
    details = []
    if target_tone == 'friendly':
        if re.search(r'\b(you|your|let\'s|we)\b', text, re.I):
            score += 1
            details.append('uses friendly pronouns')
        if '!' in text:
            score += 1
            details.append('enthusiastic punctuation')
    if target_tone == 'professional':
        if re.search(r'\b(provide|ensure|guarantee|service|support)\b', text, re.I):
            score += 1
            details.append('professional keywords')
        if len(text.split()) > 20:
            score += 1
            details.append('sufficient length')
    # ... Add more rules for other tones as needed
    entry = {
        'timestamp': datetime.datetime.utcnow().isoformat() + 'Z',
        'text': text,
        'target_tone': target_tone,
        'score': score,
        'details': details
    }
    with open(TONE_LOG, 'a') as f:
        f.write(json.dumps(entry) + '\n')
    return score, details
