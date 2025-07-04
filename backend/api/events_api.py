from fastapi import APIRouter, Request
from core.event_router import EventRouter
from datetime import datetime
from fastapi.responses import JSONResponse
import logging
from integrations.webhooks import verify_webhook_signature

router = APIRouter()
event_router = EventRouter()

@router.get('/api/events/log')
def get_event_log():
    # Fetch from Redis or SQLite
    try:
        events = []
        # Try Redis first
        if event_router.redis:
            logs = event_router.redis.lrange('event_log', 0, -1)
            for i, l in enumerate(logs):
                entry = event_router.db.execute('SELECT ts, event, payload FROM event_log WHERE rowid=?', (i+1,)).fetchone()
                if entry:
                    payload = entry[2]
                else:
                    payload = l
                events.append({
                    'id': i,
                    'timestamp': entry[0] if entry else datetime.utcnow().isoformat(),
                    'event_type': entry[1] if entry else 'unknown',
                    'payload': payload,
                    'status': 'success',
                    'integrations': []
                })
        else:
            cursor = event_router.db.cursor()
            cursor.execute('SELECT rowid, ts, event, payload FROM event_log ORDER BY ts DESC LIMIT 200')
            for row in cursor.fetchall():
                events.append({
                    'id': row[0],
                    'timestamp': row[1],
                    'event_type': row[2],
                    'payload': row[3],
                    'status': 'success',
                    'integrations': []
                })
        return JSONResponse(events)
    except Exception:
        return JSONResponse([], status_code=500)

@router.post('/api/events/retrigger')
def retrigger_event(req: Request):
    payload_bytes = req.body() if hasattr(req, 'body') else b''
    sig = req.headers.get('x-hub-signature')
    if not verify_webhook_signature(payload_bytes, sig):
        logging.warning(f"HMAC validation failed for /api/events/retrigger from {req.client.host if hasattr(req, 'client') else 'unknown'}")
        return JSONResponse({"detail": "Invalid or missing signature."}, status_code=403)
    try:
        data = req.json()
    except Exception:
        return JSONResponse({"detail": "Malformed JSON."}, status_code=400)
    event_router.manual_retrigger(data['event_type'], data['payload'])
    return {'status': 'ok'}

@router.post('/api/events/edit')
def edit_event(req: Request):
    payload_bytes = req.body() if hasattr(req, 'body') else b''
    sig = req.headers.get('x-hub-signature')
    if not verify_webhook_signature(payload_bytes, sig):
        logging.warning(f"HMAC validation failed for /api/events/edit from {req.client.host if hasattr(req, 'client') else 'unknown'}")
        return JSONResponse({"detail": "Invalid or missing signature."}, status_code=403)
    try:
        data = req.json()
    except Exception:
        return JSONResponse({"detail": "Malformed JSON."}, status_code=400)
    event_router.manual_retrigger(data['event_type'], data['payload'])
    return {'status': 'ok'}

@router.get('/api/events/ai_insights')
def get_ai_insights():
    insights = event_router.get_latest_insights()
    return JSONResponse(insights)
