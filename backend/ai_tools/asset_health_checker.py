"""
AIFOLIO SAFE AI Asset Health Checker
Static, deterministic checker for PDF/image asset integrity.
"""
import logging
logger = logging.getLogger(__name__)
import os

def check_asset_health(asset_path: str) -> dict:
    """Static, deterministic asset health checker. Extension: real file integrity checks."""
    result = {
        'exists': os.path.exists(asset_path),
        'size_bytes': os.path.getsize(asset_path) if os.path.exists(asset_path) else 0,
        'is_pdf': asset_path.lower().endswith('.pdf'),
        'is_image': asset_path.lower().endswith(('.png', '.jpg', '.jpeg')),
        'requires_human_review': False
    }
    logger.info(f"Checked asset health for {asset_path}: {result}")
    return result
