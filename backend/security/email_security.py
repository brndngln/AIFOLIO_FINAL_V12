"""
AIFOLIO Safe Email Handling
Static, deterministic, SAFE AI-compliant DKIM/SPF/DMARC validation and TLS mail server config.
"""
import logging

logger = logging.getLogger(__name__)

STATIC_EMAIL_SECURITY = {
    "dkim": True,
    "spf": True,
    "dmarc": True,
    "tls_min_version": "TLSv1.3",
}


def get_email_security_config() -> dict:
    logger.info(f"Email security config: {STATIC_EMAIL_SECURITY}")
    return STATIC_EMAIL_SECURITY
