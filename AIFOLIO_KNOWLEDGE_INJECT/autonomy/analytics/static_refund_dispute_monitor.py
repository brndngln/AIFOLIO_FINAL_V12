"""
AIFOLIO SAFE AI Refund & Dispute Monitor
- Alerts if refund or dispute % exceeds static threshold (table-driven, non-learning)
"""


def refund_dispute_monitor(sales, refunds, disputes, threshold=0.1):
    total_sales = len(sales)
    refund_rate = len(refunds) / total_sales if total_sales else 0
    dispute_rate = len(disputes) / total_sales if total_sales else 0
    alert = refund_rate > threshold or dispute_rate > threshold
    return {"refund_rate": refund_rate, "dispute_rate": dispute_rate, "alert": alert}
