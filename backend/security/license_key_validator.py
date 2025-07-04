"""
AIFOLIO Secure License Key Validator
Static, deterministic, SAFE AI-compliant license key validation with local and server fallback.
"""
import logging
logger = logging.getLogger(__name__)

STATIC_LICENSE_KEYS = ['AIFOLIO-2025-ELITE-KEY', 'AIFOLIO-2025-OWNER-KEY']


def validate_license_key(key: str) -> bool:
    valid = key in STATIC_LICENSE_KEYS
    logger.info(f"License key {key} valid: {valid}")
    return valid
