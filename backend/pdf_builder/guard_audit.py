import json
import os
from collections import Counter

SAFETY_LOG = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../analytics/ai_safety_log.jsonl'))

def summarize_guard_blocks():
    if not os.path.exists(SAFETY_LOG):
        print("No ai_safety_log.jsonl found.")
        return
    pattern_counts = Counter()
    category_counts = Counter()
    with open(SAFETY_LOG, 'r') as f:
        for line in f:
            entry = json.loads(line)
            if not entry.get('safe', True):
                for pat in entry.get('patterns_detected', []):
                    pattern_counts[pat] += 1
                for cat in entry.get('categories', []):
                    category_counts[cat] += 1
    print("Blocked Patterns:")
    for pat, count in pattern_counts.most_common():
        print(f"{pat}: {count}")
    print("\nBlocked Categories:")
    for cat, count in category_counts.most_common():
        print(f"{cat}: {count}")
