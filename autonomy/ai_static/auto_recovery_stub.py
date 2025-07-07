"""
AIFOLIO™ SAFE AI MODULE: Auto-Recovery Stub
- Static, non-sentient
- Logs failed jobs and suggests manual recovery steps
- No autonomous retries or repair
"""
import logging

LOG_PATH = "../../distribution/legal_exports/auto_recovery_log.txt"
logging.basicConfig(filename=LOG_PATH, level=logging.INFO)


from typing import Any

def log_failed_job(job_id: str, error: str) -> None:
    logging.warning(f"Job {job_id} failed: {error}")
    # Suggest manual recovery steps (no automation)
    logging.info(f"Suggested action: Review logs and restart job {job_id} manually.")
