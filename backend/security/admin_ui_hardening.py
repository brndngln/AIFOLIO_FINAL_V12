"""
AIFOLIO Admin UI Security Hardening
Static, deterministic, SAFE AI-compliant admin UI hardening with IP whitelisting and static route guards.
"""
import logging
logger = logging.getLogger(__name__)

STATIC_ADMIN_IP_WHITELIST = ['192.168.1.100', '10.0.0.5']
STATIC_ADMIN_ROUTES = ['/admin', '/dashboard/admin', '/api/admin']


def is_ip_whitelisted(ip: str) -> bool:
    allowed = ip in STATIC_ADMIN_IP_WHITELIST
    logger.info(f"IP whitelist check for {ip}: {allowed}")
    return allowed

def is_admin_route(route: str) -> bool:
    allowed = route in STATIC_ADMIN_ROUTES
    logger.info(f"Admin route check for {route}: {allowed}")
    return allowed
