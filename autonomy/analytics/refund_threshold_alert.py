"""
AIFOLIO SAFE AI Refund Threshold Alerting
- Alerts if refund % exceeds static threshold (no learning)
"""


from typing import List, Dict, Any

def refund_threshold_alert(
    vault_id: str, sales: List[Dict[str, Any]], refunds: List[Dict[str, Any]], threshold: float = 0.1
) -> Dict[str, Any]:
    """
    SAFE AI-compliant: Static refund threshold alert. Deterministic, owner-controlled, no adaptive logic.
    """
    total_sales = len(sales)
    refund_rate = len(refunds) / total_sales if total_sales else 0.0
    alert = refund_rate > threshold
    return {"vault_id": vault_id, "refund_rate": refund_rate, "alert": alert}
