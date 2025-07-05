import json
import datetime
import os

REFUND_OPT_LOG = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__), "../../analytics/gumroad_refund_optimizer_log.jsonl"
    )
)
os.makedirs(os.path.dirname(REFUND_OPT_LOG), exist_ok=True)


# --- Gumroad Refund Optimizer AI (Suggest-Only, Non-Sentient) ---
def suggest_refund_action(refund_reason, sale_metadata):
    """
    Pattern-based refund suggestion. Never auto-triggers refunds; only suggests for admin review.
    """
    suggestion = "review"
    if "download issue" in refund_reason.lower():
        suggestion = "possible tech support"
    elif "not as described" in refund_reason.lower():
        suggestion = "possible partial refund"
    elif "duplicate" in refund_reason.lower():
        suggestion = "deny/refund duplicate"
    entry = {
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "refund_reason": refund_reason,
        "sale_metadata": sale_metadata,
        "suggestion": suggestion,
    }
    with open(REFUND_OPT_LOG, "a") as f:
        f.write(json.dumps(entry) + "\n")
    return suggestion


if __name__ == "__main__":
    print(suggest_refund_action("Not as described", {"order_id": "123"}))
