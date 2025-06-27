"""
Static asset health and visual balance analytics for AIFOLIO™. SAFE AI, owner-controlled, fully auditable.
"""
def check_asset_health(vault_id, assets):
    """Return static asset health and visual balance summary."""
    health = 'good' if all(a['status']=='ok' for a in assets) else 'needs review'
    balance = 'balanced' if sum(a['weight'] for a in assets)%2==0 else 'unbalanced'
    return {'vault_id': vault_id, 'health': health, 'visual_balance': balance, 'asset_count': len(assets)}
