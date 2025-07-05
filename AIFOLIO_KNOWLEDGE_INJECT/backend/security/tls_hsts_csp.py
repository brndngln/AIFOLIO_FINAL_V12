"""
AIFOLIO TLS/HSTS/CSP Security
Static, deterministic, SAFE AI-compliant strict transport and content security policy config.
"""
import logging

logger = logging.getLogger(__name__)

STATIC_TLS_CONFIG = {
    "min_version": "TLSv1.3",
    "hsts": "max-age=31536000; includeSubDomains",
    "csp": "default-src 'self'; script-src 'self'; object-src 'none';",
}


def get_tls_security_config() -> dict:
    logger.info(f"TLS/HSTS/CSP config: {STATIC_TLS_CONFIG}")
    return STATIC_TLS_CONFIG
