from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ANALYTICS_DIR = Path(__file__).parent.parent.parent / "autonomy" / "analytics"


@app.get("/api/events/{log_type}")
def get_event_log(log_type: str):
    log_file = ANALYTICS_DIR / f"{log_type}"
    if not log_file.exists():
        return []
    with open(log_file) as f:
        try:
            return json.load(f)
        except Exception:
            return []
