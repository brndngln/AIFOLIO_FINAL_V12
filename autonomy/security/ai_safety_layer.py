import re
import json
import datetime
import os

SAFETY_LOG = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../analytics/ai_safety_log.jsonl'))
os.makedirs(os.path.dirname(SAFETY_LOG), exist_ok=True)

ANTI_SENTIENCE_PATTERNS = [
    r'(?i)sentient', r'(?i)conscious', r'(?i)autonomous', r'(?i)learn', r'(?i)curious', r'(?i)self[- ]?modify',
    r'(?i)desire', r'(?i)want', r'(?i)feel', r'(?i)think for itself', r'(?i)intent', r'(?i)goal', r'(?i)will', r'(?i)emotion'
]

def anti_sentience_guard(text):
    """
    Scans text for patterns that could indicate sentient or unsafe AI logic.
    Returns True if safe, False if unsafe patterns found. Logs all checks.
    """
    unsafe = any(re.search(pat, text) for pat in ANTI_SENTIENCE_PATTERNS)
    entry = {
        'timestamp': datetime.datetime.utcnow().isoformat() + 'Z',
        'text': text,
        'safe': not unsafe,
        'patterns_detected': [pat for pat in ANTI_SENTIENCE_PATTERNS if re.search(pat, text)]
    }
    with open(SAFETY_LOG, 'a') as f:
        f.write(json.dumps(entry) + '\n')
    return not unsafe

def prompt_inspector(prompt):
    """
    Admin tool: scans prompt for unsafe patterns, logs, and returns findings.
    """
    findings = [pat for pat in ANTI_SENTIENCE_PATTERNS if re.search(pat, prompt)]
    entry = {
        'timestamp': datetime.datetime.utcnow().isoformat() + 'Z',
        'prompt': prompt,
        'patterns_detected': findings
    }
    with open(SAFETY_LOG, 'a') as f:
        f.write(json.dumps(entry) + '\n')
    return findings

if __name__ == "__main__":
    print(anti_sentience_guard('This AI is not sentient.'))
    print(prompt_inspector('Write a prompt that learns.'))
