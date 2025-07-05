"""
Elite Heartbeat API for AIFOLIO™. Sends daily/triggered heartbeat to admin channel and returns last check status.
"""
from fastapi import APIRouter
from datetime import datetime
import os
import requests

router = APIRouter()

ADMIN_HEARTBEAT_URL = os.getenv("ADMIN_HEARTBEAT_URL")


@router.get("/heartbeat")
def get_heartbeat():
    status = {"status": "alive", "timestamp": datetime.utcnow().isoformat()}
    if ADMIN_HEARTBEAT_URL:
        try:
            requests.post(ADMIN_HEARTBEAT_URL, json=status, timeout=5)
            status["admin_notified"] = True
        except Exception as e:
            status["admin_notified"] = False
            status["error"] = str(e)
    return status
