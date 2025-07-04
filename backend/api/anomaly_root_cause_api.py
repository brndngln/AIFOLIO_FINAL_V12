from fastapi import APIRouter, Query
<<<<<<< HEAD
from backend.ai.anomaly_root_cause import analyze_all, analyze_anomaly
from pathlib import Path
import json
=======
from backend.ai.anomaly_root_cause import analyze_all
>>>>>>> omni_repair_backup_20250704_1335

router = APIRouter()

@router.get('/api/anomaly/root_cause')
def root_cause_all():
    return analyze_all()

@router.get('/api/anomaly/root_cause_one')
def root_cause_one(idx: int = Query(0)):
    results = analyze_all()
    if 0 <= idx < len(results):
        return results[idx]
    return {}
