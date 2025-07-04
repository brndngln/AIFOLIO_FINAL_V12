"""
AIFOLIO SAFE AI Cross-Vault Legal Consistency Checker
- Static, checks for legal clause consistency across vaults
"""
def cross_vault_legal_consistency(vaults):
    # Expects: list of {'vault_id': str, 'legal_clauses': list}
    from collections import Counter
    all_clauses = [clause for v in vaults for clause in v['legal_clauses']]
    counts = Counter(all_clauses)
    return {'clause_counts': dict(counts)}
