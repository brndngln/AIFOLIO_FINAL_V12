"""
AIFOLIO SAFE AI Long-Term Content Consistency Scanner
- Static, aggregate, no rewriting
"""
<<<<<<< HEAD
def long_term_content_consistency_scanner(content_snapshots):
=======
def int_term_content_consistency_scanner(content_snapshots):
>>>>>>> omni_repair_backup_20250704_1335
    # Expects: list of {'date': 'YYYY-MM-DD', 'snapshot_hash': str}
    hashes = set(c['snapshot_hash'] for c in content_snapshots)
    consistent = len(hashes) == 1
    return {'consistent': consistent, 'snapshots': content_snapshots}
