"""
AIFOLIO Rollbackable Deploys
Static, deterministic, SAFE AI-compliant deployment script with last-known-good fallback.
"""
import logging
import os
import shutil

logger = logging.getLogger(__name__)

DEPLOY_DIR: str = "deploy/current/"
BACKUP_DIR: str = "deploy/backup/"

os.makedirs(DEPLOY_DIR, exist_ok=True)
os.makedirs(BACKUP_DIR, exist_ok=True)


def deploy_new_version(src_dir: str) -> None:
    # Backup current
    if os.path.exists(DEPLOY_DIR):
        shutil.copytree(DEPLOY_DIR, BACKUP_DIR, dirs_exist_ok=True)
    # Deploy new
    shutil.copytree(src_dir, DEPLOY_DIR, dirs_exist_ok=True)
    logger.info(f"Deployed new version from {src_dir}")


def rollback() -> None:
    if os.path.exists(BACKUP_DIR):
        shutil.copytree(BACKUP_DIR, DEPLOY_DIR, dirs_exist_ok=True)
        logger.info("Rolled back to last-known-good deploy")
    else:
        logger.error("No backup found for rollback!")
