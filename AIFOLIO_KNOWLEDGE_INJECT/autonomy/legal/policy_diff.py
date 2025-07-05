import os
import difflib
import json
from datetime import datetime

POLICY_FILES = ["terms_of_service.md", "refund_policy.md", "privacy_policy.md"]

HISTORY_PATH = os.path.join(os.path.dirname(__file__), "policy_history.json")


def diff_policies(policy_name: str, old_version: str, new_version: str) -> str:
    """
    Returns a unified diff between two versions of a policy.
    """
    old_lines = old_version.splitlines()
    new_lines = new_version.splitlines()
    diff = difflib.unified_diff(
        old_lines, new_lines, fromfile="old", tofile="new", lineterm=""
    )
    return "\n".join(diff)


def record_policy_version(policy_name: str, content: str, hash: str):
    """
    Append a new version to the policy history with timestamp and hash.
    """
    if os.path.exists(HISTORY_PATH):
        with open(HISTORY_PATH, "r") as f:
            history = json.load(f)
    else:
        history = {"history": []}
    history["history"].append(
        {
            "policy_name": policy_name,
            "timestamp": datetime.utcnow().isoformat(),
            "hash": hash,
            "content": content,
        }
    )
    with open(HISTORY_PATH, "w") as f:
        json.dump(history, f, indent=2)
