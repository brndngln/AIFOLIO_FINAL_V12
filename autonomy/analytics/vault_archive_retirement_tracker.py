"""
AIFOLIO SAFE AI Vault Archive / Retirement Tracker
- Flags vaults for archiving/retirement (static)
"""
def vault_archive_retirement(vaults):
    # Expects: list of {'vault_id': str, 'last_active': 'YYYY-MM-DD'}
    import datetime
    today = datetime.datetime.now().date()
    flagged = [v for v in vaults if (today - datetime.datetime.strptime(v['last_active'], '%Y-%m-%d').date()).days > 730]
    return {'archive_candidates': flagged}
