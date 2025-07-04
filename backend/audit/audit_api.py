# audit_api.py
# FastAPI endpoints for audit log retrieval (founder-only)
<<<<<<< HEAD
from fastapi import APIRouter, Depends, HTTPException
import os, json
=======
from fastapi import APIRouter
import os
import json
>>>>>>> omni_repair_backup_20250704_1335

router = APIRouter()
AUDIT_LOG_PATH = os.path.join(os.path.dirname(__file__), '../../audit.log')

@router.get('/audit/logs')
def get_audit_logs():
    # In production: enforce founder-only access
    with open(AUDIT_LOG_PATH) as f:
        return [json.loads(line) for line in f.readlines()]
