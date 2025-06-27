"""
Static, deterministic churn and retention analytics for AIFOLIO™. SAFE AI, owner-controlled, fully auditable.
"""
def calculate_churn_retention(vault_id, user_events, period_days=30):
    """Return static churn rate, retention cohort, and LTV for a vault."""
    total_users = len(set(e['user_id'] for e in user_events if e['vault_id']==vault_id))
    churned = len([e for e in user_events if e['vault_id']==vault_id and e['event']=='churn'])
    retained = total_users - churned
    churn_rate = (churned / total_users) if total_users else 0
    ltv = retained * 100  # static LTV formula
    return {'vault_id': vault_id, 'churn_rate': churn_rate, 'retained': retained, 'ltv': ltv, 'period_days': period_days}
