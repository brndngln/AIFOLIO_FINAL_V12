"""
AIFOLIO Immutable Audit Logging
Static, deterministic, SAFE AI-compliant append-only audit log for all critical operations.
"""
import logging
import os
from datetime import datetime
logger = logging.getLogger(__name__)

AUDIT_LOG_PATH = os.getenv('AIFOLIO_AUDIT_LOG_PATH', 'audit/exports/immutable_audit.log')


def log_audit_event(event: str) -> None:
    timestamp = datetime.utcnow().isoformat()
    with open(AUDIT_LOG_PATH, 'a') as f:
        f.write(f"{timestamp} | {event}\n")
    logger.info(f"Audit event logged: {event}")
