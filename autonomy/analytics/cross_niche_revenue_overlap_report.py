"""
AIFOLIO SAFE AI Cross-Niche Revenue Overlap Report
- Static, aggregate, admin-reviewed
"""
def cross_niche_revenue_overlap(niche_sales):
    # Expects: dict of {'niche': set(vault_ids)}
    overlap = {}
    niches = list(niche_sales.keys())
    for i, n1 in enumerate(niches):
        for n2 in niches[i+1:]:
            overlap_key = f"{n1} & {n2}"
            overlap[overlap_key] = len(set(niche_sales[n1]) & set(niche_sales[n2]))
    return {'cross_niche_overlap': overlap}
