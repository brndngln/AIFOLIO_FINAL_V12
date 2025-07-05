"""
AIFOLIO SAFE AI Legal Compliance Heatmap
- Shows vault-by-vault % compliance (static)
"""


def legal_compliance_heatmap(vaults):
    # Expects: list of {'vault_id': str, 'compliance': float}
    heatmap = {v["vault_id"]: v["compliance"] for v in vaults}
    return heatmap
