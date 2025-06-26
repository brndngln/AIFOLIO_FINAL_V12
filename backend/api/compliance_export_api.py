from fastapi import APIRouter, Query, Response
from pathlib import Path
import json
import zipfile
import io
from datetime import datetime

router = APIRouter()
LOG_PATH = Path(__file__).parent.parent.parent / 'logs' / 'secret_rotation.json'
ANOMALY_PATH = Path(__file__).parent.parent.parent / 'logs' / 'usage_anomalies.json'
OVERRIDE_PATH = Path(__file__).parent.parent.parent / 'logs' / 'override_attempts.json'

@router.get('/api/compliance/export', response_class=Response)
def compliance_export():
    files = [
        ('secret_rotation.json', LOG_PATH),
        ('usage_anomalies.json', ANOMALY_PATH),
        ('override_attempts.json', OVERRIDE_PATH)
    ]
    mem_zip = io.BytesIO()
    with zipfile.ZipFile(mem_zip, mode='w', compression=zipfile.ZIP_DEFLATED) as zf:
        for name, path in files:
            if path.exists():
                with open(path, 'r') as f:
                    zf.writestr(name, f.read())
    mem_zip.seek(0)
    ts = datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')
    return Response(content=mem_zip.read(), media_type='application/zip', headers={
        'Content-Disposition': f'attachment; filename="aifolio_compliance_export_{ts}.zip"'
    })
