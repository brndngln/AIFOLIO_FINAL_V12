"""
AIFOLIO SAFE AI Time-to-Purchase Metrics
- Aggregate only, no profiling
"""


def time_to_purchase_metrics(events):
    # Expects: list of {'buyer_id': str, 'first_view': 'YYYY-MM-DD', 'purchase': 'YYYY-MM-DD'}
    from datetime import datetime

    times = []
    for e in events:
        if e.get("first_view") and e.get("purchase"):
            fv = datetime.strptime(e["first_view"], "%Y-%m-%d")
            p = datetime.strptime(e["purchase"], "%Y-%m-%d")
            times.append((p - fv).days)
    avg = sum(times) / len(times) if times else 0
    return {"average_days_to_purchase": avg}
