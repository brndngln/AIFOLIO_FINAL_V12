"""
AIFOLIO Endpoint Cloaking Layer
Static, deterministic, SAFE AI-compliant endpoint cloaking config and audit logger.
"""
import logging

logger = logging.getLogger(__name__)

STATIC_ENDPOINT_MAP = {
    "/api/vault": "/api/v1a9f2/vault",
    "/api/admin": "/api/v1a9f2/admin",
    "/dashboard": "/dash/secure-9f2",
    "/login": "/auth/secure-1f8",
}


def get_cloaked_endpoint(endpoint: str) -> str:
    cloaked = STATIC_ENDPOINT_MAP.get(endpoint, endpoint)
    logger.info(f"Cloaked endpoint for {endpoint}: {cloaked}")
    return cloaked
