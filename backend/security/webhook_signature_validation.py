"""
AIFOLIO Webhook Signature Validation
Static, deterministic, SAFE AI-compliant HMAC SHA256 signature validation for webhooks.
"""
import logging
import hmac
import hashlib
import os
logger = logging.getLogger(__name__)

SECRET = os.getenv('AIFOLIO_WEBHOOK_SECRET', 'staticsecret')

def validate_signature(payload: bytes, signature: str) -> bool:
    mac = hmac.new(SECRET.encode(), msg=payload, digestmod=hashlib.sha256)
    expected = mac.hexdigest()
    valid = hmac.compare_digest(expected, signature)
    logger.info(f"Webhook signature valid: {valid}")
    return valid
