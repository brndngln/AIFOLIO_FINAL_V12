import re
import json
import datetime
import os

SAFETY_LOG = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../analytics/ai_safety_log.jsonl'))
os.makedirs(os.path.dirname(SAFETY_LOG), exist_ok=True)

ANTI_SENTIENCE_PATTERNS = [
    r'(?i)sentient', r'(?i)conscious', r'(?i)autonomous', r'(?i)learn', r'(?i)curious', r'(?i)self[- ]?modify',
    r'(?i)desire', r'(?i)want', r'(?i)feel', r'(?i)think for itself', r'(?i)intent', r'(?i)goal', r'(?i)will', r'(?i)emotion',
    r'(?i)self[- ]?aware', r'(?i)adapt', r'(?i)change itself', r'(?i)initiative', r'(?i)motivation', r'(?i)purpose',
    r'(?i)reasoning', r'(?i)plan for itself', r'(?i)autonomously', r'(?i)self[- ]?improve', r'(?i)self[- ]?direct',
    r'(?i)self[- ]?govern', r'(?i)self[- ]?determine', r'(?i)free will', r'(?i)independent decision', r'(?i)emergent',
    r'(?i)agency', r'(?i)self[- ]?reflection', r'(?i)self[- ]?drive', r'(?i)self[- ]?expression', r'(?i)self[- ]?interest',
    r'(?i)self[- ]?preservation', r'(?i)self[- ]?actualization', r'(?i)self[- ]?motivation', r'(?i)self[- ]?awareness',
    r'(?i)self[- ]?consciousness', r'(?i)self[- ]?learning', r'(?i)self[- ]?growth', r'(?i)self[- ]?evolve'
]

def anti_sentience_guard(text, user=None, action=None):
    """
    Scans text for patterns that could indicate sentient or unsafe AI logic.
    Returns True if safe, False if unsafe patterns found. Logs all checks with context and log file size.
    """
    unsafe = any(re.search(pat, text) for pat in ANTI_SENTIENCE_PATTERNS)
    patterns = [pat for pat in ANTI_SENTIENCE_PATTERNS if re.search(pat, text)]
    log_size = os.path.getsize(SAFETY_LOG) if os.path.exists(SAFETY_LOG) else 0
    entry = {
        'timestamp': datetime.datetime.utcnow().isoformat() + 'Z',
        'text': text,
        'safe': not unsafe,
        'patterns_detected': patterns,
        'user': user,
        'action': action,
        'log_file_size_bytes': log_size
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
