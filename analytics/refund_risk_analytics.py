"""
Static, deterministic refund risk analytics for AIFOLIO™. SAFE AI, owner-controlled, fully auditable.
"""
def calculate_refund_risk(vault_id, sales, refunds, period_days=30):
    """Return static refund risk score and summary for a vault."""
    if not sales:
        return {'vault_id': vault_id, 'risk': 'low', 'score': 0, 'reason': 'No sales in period'}
    refund_count = len([r for r in refunds if r['vault_id']==vault_id])
    risk = 'high' if refund_count > 5 else 'medium' if refund_count > 1 else 'low'
    score = min(100, refund_count * 20)
    return {'vault_id': vault_id, 'risk': risk, 'score': score, 'refunds': refund_count, 'period_days': period_days}
