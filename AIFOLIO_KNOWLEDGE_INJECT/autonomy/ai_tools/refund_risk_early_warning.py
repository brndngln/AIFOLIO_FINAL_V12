import json
import datetime
import os

RISK_LOG = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__), "../../analytics/refund_risk_early_warning_log.jsonl"
    )
)
os.makedirs(os.path.dirname(RISK_LOG), exist_ok=True)


# --- AI Refund-Risk Early Warning System (Static, Read-Only) ---
def flag_refund_risk(vault_id, sales, refunds):
    sales_count = sum(1 for s in sales if s["vault_id"] == vault_id)
    refund_count = sum(1 for r in refunds if r["vault_id"] == vault_id)
    rate = refund_count / sales_count if sales_count else 0
    risk = (
        "high"
        if rate > 0.25 and refund_count >= 3
        else "medium"
        if rate > 0.1
        else "low"
    )
    entry = {
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "vault_id": vault_id,
        "sales": sales_count,
        "refunds": refund_count,
        "refund_rate": rate,
        "risk": risk,
    }
    with open(RISK_LOG, "a") as f:
        f.write(json.dumps(entry) + "\n")
    return risk, rate
