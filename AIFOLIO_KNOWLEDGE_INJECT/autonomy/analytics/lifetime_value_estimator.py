import pandas as pd
import json
import os
import datetime

LTV_LOG = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../analytics/lifetime_value_log.jsonl")
)
os.makedirs(os.path.dirname(LTV_LOG), exist_ok=True)


# --- Lifetime Value Estimator ---
def estimate_lifetime_value(sales, refunds, customer_id):
    """
    Estimates LTV for a given customer based on sales, refunds, and time.
    sales: list of dicts {customer, amount, timestamp}
    refunds: list of dicts {customer, amount, timestamp}
    customer_id: str
    Returns: dict with LTV and summary
    """
    df_sales = pd.DataFrame([s for s in sales if s["customer"] == customer_id])
    df_refunds = pd.DataFrame([r for r in refunds if r["customer"] == customer_id])
    total_sales = df_sales["amount"].sum()
    total_refunds = df_refunds["amount"].sum() if not df_refunds.empty else 0
    ltv = total_sales - total_refunds
    entry = {
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "customer": customer_id,
        "sales": total_sales,
        "refunds": total_refunds,
        "ltv": ltv,
    }
    with open(LTV_LOG, "a") as f:
        f.write(json.dumps(entry) + "\n")
    return {"customer": customer_id, "ltv": ltv}


if __name__ == "__main__":
    print(
        estimate_lifetime_value(
            [
                {"customer": "c1", "amount": 100, "timestamp": "2025-06-21"},
                {"customer": "c1", "amount": 50, "timestamp": "2025-06-21"},
            ],
            [{"customer": "c1", "amount": 10, "timestamp": "2025-06-21"}],
            "c1",
        )
    )
