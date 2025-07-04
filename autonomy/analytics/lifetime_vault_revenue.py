"""
AIFOLIO SAFE AI Lifetime Vault Revenue Stats
- Reports lifetime revenue for each vault (static)
"""
def lifetime_vault_revenue(vaults):
    # Expects: list of {'vault_id': str, 'revenue': int}
    return {v['vault_id']: v['revenue'] for v in vaults}
