"""
AIFOLIO SAFE AI Multi-Vault Launch Planner
- Static, suggests optimal launch windows based on aggregate past launches
"""
def multi_vault_launch_plan(launch_history):
    # Expects: list of {'vault_id': str, 'launch_date': 'YYYY-MM-DD'}
    from collections import Counter
    import datetime
    if not launch_history:
        return {'suggested_month': None}
    months = [datetime.datetime.strptime(l['launch_date'], '%Y-%m-%d').month for l in launch_history]
    most_common = Counter(months).most_common(1)
    return {'suggested_month': most_common[0][0] if most_common else None}
