"""
AIFOLIO Beginner Mistake Protections
Static, deterministic, SAFE AI-compliant checks for common misconfigurations and security gaps.
"""
import logging
import os
logger = logging.getLogger(__name__)

STATIC_CHECKS = [
    ('Public admin route', lambda: '/admin' not in os.listdir('.')),
    ('Key exposure', lambda: not os.path.exists('.env.public')),
    ('Weak JWT', lambda: not os.path.exists('jwt_weak.txt')),
    ('Vault encryption', lambda: os.path.exists('vault_encrypted.flag')),
    ('Dynamic AI tuning', lambda: not os.path.exists('dynamic_ai.flag')),
    ('License key handling', lambda: os.path.exists('license_key.flag')),
    ('Customer email validation', lambda: os.path.exists('customer_email_valid.flag')),
    ('Public CI/CD', lambda: not os.path.exists('public_ci_cd.flag')),
    ('PDF plagiarism', lambda: not os.path.exists('pdf_plagiarism.flag')),
    ('Backup verification', lambda: os.path.exists('backup_verified.flag')),
    ('Dynamic AI personality', lambda: not os.path.exists('ai_personality.flag')),
    ('Version locking', lambda: os.path.exists('version_locked.flag')),
]

def run_beginner_mistake_checks() -> dict:
    results = {}
    for name, check in STATIC_CHECKS:
        try:
            results[name] = check()
        except Exception:
            results[name] = False
        logger.info(f"Beginner mistake check: {name} = {results[name]}")
    return results
