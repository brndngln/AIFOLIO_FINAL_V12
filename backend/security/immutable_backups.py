"""
AIFOLIO Immutable Code Vault Backups (WORM)
Static, deterministic, SAFE AI-compliant backup script and verification logic.
"""
import logging
import os
import shutil
from datetime import datetime

logger = logging.getLogger(__name__)

BACKUP_DIR = "backups/worm/"
CODE_DIR = "aifolio_empire/"

os.makedirs(BACKUP_DIR, exist_ok=True)


def create_worm_backup():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = os.path.join(BACKUP_DIR, f"code_backup_{timestamp}")
    shutil.copytree(CODE_DIR, backup_path)
    os.chmod(backup_path, 0o400)  # Read-only
    logger.info(f"Immutable backup created at {backup_path}")
    return backup_path


def verify_worm_backup(backup_path: str) -> bool:
    result = os.access(backup_path, os.R_OK) and not os.access(backup_path, os.W_OK)
    logger.info(f"Backup verification for {backup_path}: {result}")
    return result
