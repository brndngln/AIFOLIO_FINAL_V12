"""
Phase 9+ SAFE AI Audit Log Streaming (static, SAFE AI compliant)
- Provides a static, polling-based streaming endpoint for the audit log
- No adaptive logic; fully auditable and static
"""
import time
from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import StreamingResponse

audit_router = APIRouter()

@audit_router.get("/phase9/audit_log/stream")
def stream_audit_log(request: Request):
    def event_stream():
        logfile = "distribution/legal_exports/phase9_empire_audit_log.txt"
        last_pos = 0
        while True:
            try:
                with open(logfile, "r") as f:
                    f.seek(last_pos)
                    lines = f.readlines()
                    if lines:
                        for line in lines:
                            yield f"data: {line.strip()}\n\n"
                        last_pos = f.tell()
            except Exception:
                pass
            time.sleep(2)  # Poll every 2 seconds
            if await_disconnect(request):
                break
    return StreamingResponse(event_stream(), media_type="text/event-stream")

def await_disconnect(request):
    if hasattr(request, 'is_disconnected'):
        return request.is_disconnected()
    return False
