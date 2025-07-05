"""
AIFOLIO™ SAFE AI MODULE: Refund Optimizer
- Static, non-sentient, pattern-based only
- Suggests refund actions based on static rules (no learning)
- Logs all suggestions for human approval
"""
import logging
import json

LOG_PATH = "../../distribution/legal_exports/refund_optimizer_log.txt"
logging.basicConfig(filename=LOG_PATH, level=logging.INFO)


def suggest_refund_action(refund_log_path):
    with open(refund_log_path, "r") as f:
        refunds = json.load(f)
    suggestions = []
    for refund in refunds:
        if refund.get("reason") == "duplicate" and refund.get("amount", 0) < 100:
            suggestions.append({"id": refund["id"], "action": "auto-approve"})
        elif refund.get("reason") == "fraud":
            suggestions.append({"id": refund["id"], "action": "flag-for-review"})
        else:
            suggestions.append({"id": refund["id"], "action": "manual-review"})
    logging.info(f"Refund suggestions: {suggestions}")
    return suggestions
