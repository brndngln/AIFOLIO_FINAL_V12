"""
AIFOLIO SAFE AI Competitive Vault Overlap Report
- Manual input only, static
"""


def competitive_vault_overlap(our_vaults, competitor_vaults):
    # Expects: lists of vault names
    overlap = set(our_vaults) & set(competitor_vaults)
    return {"overlap": list(overlap)}
