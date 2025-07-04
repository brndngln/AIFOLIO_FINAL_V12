"""
AIFOLIO SAFE AI Expiring Legal Clauses Tracker
- Flags legal clauses nearing expiry
"""
def expiring_legal_clauses(clauses):
    # Expects: list of {'clause_id': str, 'expiry': 'YYYY-MM-DD'}
    import datetime
    today = datetime.datetime.now().date()
    flagged = [c for c in clauses if (datetime.datetime.strptime(c['expiry'], '%Y-%m-%d').date() - today).days < 30]
    return {'expiring_clauses': flagged}
