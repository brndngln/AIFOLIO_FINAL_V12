"""
AIFOLIO™ SAFE AI MODULE: Policy Version Tracker
- Tracks and displays version history for all legal policies.
- Static only. No sentience, recursion, or adaptive logic.
- All changes logged for auditability.
"""
import os
import json
import logging
from datetime import datetime

LOG_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../distribution/legal_exports/policy_version_log.json'))
logging.basicConfig(filename=LOG_PATH.replace('.json', '.txt'), level=logging.INFO)

POLICIES = [
    "terms_of_service.md",
    "refund_policy.md",
    "privacy_policy.md"
]

VERSION_TRACKER_PATH = LOG_PATH

def record_policy_version(policy_dir, policy_name):
    path = os.path.join(policy_dir, policy_name)
    if not os.path.exists(path):
        return False
    with open(path, 'r') as f:
        content = f.read()
    version_entry = {
        "policy": policy_name,
        "timestamp": datetime.utcnow().isoformat(),
        "content_hash": hash(content)
    }
    if os.path.exists(VERSION_TRACKER_PATH):
        with open(VERSION_TRACKER_PATH, 'r') as f:
            history = json.load(f)
    else:
        history = []
    history.append(version_entry)
    with open(VERSION_TRACKER_PATH, 'w') as f:
        json.dump(history, f, indent=2)
    logging.info(f"Version recorded for {policy_name}")
    return True

def get_policy_versions():
    if os.path.exists(VERSION_TRACKER_PATH):
        with open(VERSION_TRACKER_PATH, 'r') as f:
            return json.load(f)
    return []
