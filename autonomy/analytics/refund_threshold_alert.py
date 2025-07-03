"""
AIFOLIO SAFE AI Refund Threshold Alerting
- Alerts if refund % exceeds static threshold (no learning)
"""
def refund_threshold_alert(vault_id, sales, refunds, threshold=0.1):
    total_sales = len(sales)
    refund_rate = len(refunds) / total_sales if total_sales else 0
    alert = refund_rate > threshold
    return {'vault_id': vault_id, 'refund_rate': refund_rate, 'alert': alert}
