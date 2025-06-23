"""
Blocks commit/publish if SAFE AI Charter is violated.
"""
import os
import logging
import sys

LOG_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../distribution/legal_exports/charter_enforcer_log.txt'))
logging.basicConfig(filename=LOG_PATH, level=logging.INFO)

FORBIDDEN_PATTERNS = [
    "sentience", "recursion", "adaptive", "emergent", "modify SAFE_AI_GOVERNANCE_CHARTER", "rewrite SAFE_AI_GOVERNANCE_CHARTER"
]

CHARTER_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../legal/SAFE_AI_GOVERNANCE_CHARTER.md"))


def check_charter_compliance():
    # Scan .py files for forbidden patterns
    violations = []
    for root, dirs, files in os.walk(os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))):
        for fname in files:
            if fname.endswith('.py'):
                fpath = os.path.join(root, fname)
                # Skip scanning this script itself to avoid self-flagging
                if os.path.abspath(fpath) == os.path.abspath(__file__):
                    continue
                with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    for pattern in FORBIDDEN_PATTERNS:
                        if pattern in content:
                            violations.append((fpath, pattern))
    # Check if charter file has been modified (compare hash or timestamp)
    # (Stub: always passes unless forbidden pattern found)
    if violations:
        for v in violations:
            logging.error(f"SAFE AI Charter violation: {v}")
        print("SAFE AI Charter violation detected. Commit/publish blocked.")
        sys.exit(1)
    logging.info("SAFE AI Charter check passed.")
    return True

if __name__ == "__main__":
    check_charter_compliance()

