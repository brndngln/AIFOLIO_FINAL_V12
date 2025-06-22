"""
AIFOLIO SAFE AI Risk / Refund Monitor
- Tracks refund rates and static risk flags (no optimization)
"""
def risk_refund_monitor(vaults, refunds):
    # Expects: vaults=[{'vault_id': str}], refunds=[{'vault_id': str}]
    refund_counts = {}
    for r in refunds:
        refund_counts[r['vault_id']] = refund_counts.get(r['vault_id'], 0) + 1
    risk = {v['vault_id']: {'refunds': refund_counts.get(v['vault_id'], 0)} for v in vaults}
    return risk
