from fastapi import APIRouter, Request
from core.event_router import EventRouter
from datetime import datetime
from fastapi.responses import JSONResponse

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
    except Exception as e:
        return JSONResponse([], status_code=500)

@router.post('/api/events/retrigger')
def retrigger_event(req: Request):
    data = req.json()
    event_router.manual_retrigger(data['event_type'], data['payload'])
    return {'status': 'ok'}

@router.post('/api/events/edit')
def edit_event(req: Request):
    data = req.json()
    event_router.manual_retrigger(data['event_type'], data['payload'])
    return {'status': 'ok'}

@router.get('/api/events/ai_insights')
def get_ai_insights():
    insights = event_router.get_latest_insights()
    return JSONResponse(insights)
