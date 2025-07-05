"""
AIFOLIO SAFE AI Vault Renewal Opportunity Finder
- Static, aggregate, flags vaults with renewal potential
"""


def vault_renewal_opportunity(vaults):
    # Expects: list of {'vault_id': str, 'last_renewal': 'YYYY-MM-DD', 'revenue': int}
    import datetime

    today = datetime.datetime.now().date()
    flagged = [
        v
        for v in vaults
        if (
            today - datetime.datetime.strptime(v["last_renewal"], "%Y-%m-%d").date()
        ).days
        > 365
        and v["revenue"] > 0
    ]
    return {"renewal_candidates": flagged}
