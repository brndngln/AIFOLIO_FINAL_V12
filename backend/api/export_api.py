from fastapi import APIRouter, Query, Response
from pathlib import Path
import json

router = APIRouter()
LOG_PATH = Path(__file__).parent.parent.parent / 'logs' / 'secret_rotation.json'
ANOMALY_PATH = Path(__file__).parent.parent.parent / 'logs' / 'usage_anomalies.json'
OVERRIDE_PATH = Path(__file__).parent.parent.parent / 'logs' / 'override_attempts.json'

@router.get('/api/export/audit', response_class=Response)
def export_audit(format: str = Query('json', enum=['json','csv']), log: str = Query('rotation', enum=['rotation','anomaly','override'])):
    if log == 'rotation':
        path = LOG_PATH
    elif log == 'anomaly':
        path = ANOMALY_PATH
    else:
        path = OVERRIDE_PATH
    if not path.exists():
        return Response(content='', media_type='text/plain')
    with open(path, 'r') as f:
        data = json.load(f)
    if format == 'json':
        return Response(content=json.dumps(data, indent=2), media_type='application/json')
    # CSV export
    if not data:
        return Response(content='', media_type='text/csv')
    keys = set()
    for row in data:
        keys.update(row.keys())
    keys = sorted(keys)
    out = []
    out.append(','.join(keys))
    for row in data:
        out.append(','.join(str(row.get(k,'')) for k in keys))
    return Response(content='\n'.join(out), media_type='text/csv')
