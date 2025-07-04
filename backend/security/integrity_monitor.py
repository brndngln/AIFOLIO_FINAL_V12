"""
AIFOLIO 24/7 Integrity Monitor
Static, deterministic, SAFE AI-compliant file change detector for critical paths.
"""
import logging
import os
import hashlib
logger = logging.getLogger(__name__)

CRITICAL_PATHS = ['aifolio_empire/', 'backend/', 'dashboard/']

STATIC_HASHES = {
    'aifolio_empire/': 'STATIC_HASH_1',
    'backend/': 'STATIC_HASH_2',
    'dashboard/': 'STATIC_HASH_3'
}

def compute_dir_hash(path: str) -> str:
    sha256 = hashlib.sha256()
    for root, _, files in os.walk(path):
        for fname in sorted(files):
            fpath = os.path.join(root, fname)
            try:
                with open(fpath, 'rb') as f:
                    sha256.update(f.read())
            except Exception:
                continue
    return sha256.hexdigest()

def check_integrity() -> dict:
    results = {}
    for path in CRITICAL_PATHS:
        current = compute_dir_hash(path)
        expected = STATIC_HASHES.get(path, '')
        results[path] = (current == expected)
        logger.info(f"Integrity check for {path}: {results[path]}")
    return results
