import re
import json
import datetime
import os

CORRECTOR_LOG = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../analytics/typo_grammar_corrector_log.jsonl'))
os.makedirs(os.path.dirname(CORRECTOR_LOG), exist_ok=True)

# --- AI Typo & Grammar Corrector (Static, Single-Pass) ---
COMMON_TYPO_MAP = {
    'teh': 'the',
    'recieve': 'receive',
    'adn': 'and',
    'definately': 'definitely',
    'seperate': 'separate',
    'occured': 'occurred',
    'untill': 'until',
    'wich': 'which',
    'accomodate': 'accommodate',
    'occurence': 'occurrence',
}

def correct_text(text):
    corrections = []
    for typo, corr in COMMON_TYPO_MAP.items():
        if typo in text:
            text = text.replace(typo, corr)
            corrections.append(f'{typo}→{corr}')
    # Remove double spaces
    if '  ' in text:
        text = re.sub(r' +', ' ', text)
        corrections.append('double space')
    # Capitalize first letter of sentences
    text = re.sub(r'(?:^|[.!?]\s+)([a-z])', lambda m: m.group(0).upper(), text)
    entry = {
        'timestamp': datetime.datetime.utcnow().isoformat() + 'Z',
        'original': text,
        'corrections': corrections
    }
    with open(CORRECTOR_LOG, 'a') as f:
        f.write(json.dumps(entry) + '\n')
    return text, corrections
