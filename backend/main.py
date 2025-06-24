# FastAPI backend for AIFOLIO: Secure, single-user, anti-sentient, autonomous vault automation
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import HTMLResponse
from starlette.staticfiles import StaticFiles
from passlib.context import CryptContext
import os
from typing import Optional

# --- Security Setup ---
SECRET_USERNAME = os.getenv("AIFOLIO_USER", "aifolio_owner")
SECRET_PASSWORD_HASH = os.getenv("AIFOLIO_PASSWORD_HASH", "$2b$12$Vwz5n5dYk7vYw3kz8p6e0uKj2fQe5l9d0eJrT3f8n8w2w5q6f7q6e")  # bcrypt hash for 'change_this_password'

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

app = FastAPI(title="AIFOLIO Autonomous Backend", docs_url="/docs", redoc_url="/redoc")

# --- Mount Gumroad API router ---
from api import gumroad_api
app.include_router(gumroad_api.router, prefix="/api")

# --- Mount SAFE AI PDF Builder API router ---
from backend.pdf_builder.api_pdf_builders import router as pdf_builder_router
app.include_router(pdf_builder_router)

# --- Mount SAFE AI Batches 16–20 + Partner Certification API router ---
from backend.batch_scaling.batch16_20_api import router as batch_scaling_router
app.include_router(batch_scaling_router)

# Enable CORS for local frontend dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Auth Logic ---
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def authenticate_user(username: str, password: str):
    if username != SECRET_USERNAME:
        return False
    if not verify_password(password, SECRET_PASSWORD_HASH):
        return False
    return True

from jose import jwt
from datetime import datetime, timedelta

SECRET_KEY = os.getenv("AIFOLIO_JWT_SECRET", "supersecretjwtkey")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 120

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    if not authenticate_user(form_data.username, form_data.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    # For demo, statically assign role/email/org. In production, query user profile DB.
    role = os.getenv("AIFOLIO_ROLE", "admin")
    email = os.getenv("AIFOLIO_EMAIL", "owner@aifolio.com")
    org = os.getenv("AIFOLIO_ORG", "AIFOLIO Inc.")
    access_token = create_access_token({
        "sub": form_data.username,
        "role": role,
        "email": email,
        "org": org
    })
    return {"access_token": access_token, "token_type": "bearer"}

# --- Protected Endpoint Example ---
from backend.auth.deps import get_current_user

@app.get("/api/niches")
def get_niches(user: str = Depends(get_current_user)):
    from aifolio_empire.profit_engines.automated_vault_generator import get_supported_niches
    return {"niches": get_supported_niches()}

# --- API: Generate Vault (JWT-protected) ---

from fastapi import Query, Body
from backend.admin.static_users import STATIC_USERS

STATIC_USERS_MEM = STATIC_USERS.copy()  # in-memory static list


@app.get("/admin/audit-log")
def get_audit_log(limit: int = Query(50, ge=1, le=1000), user: str = Query(None), current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Admin only")
    import os, json
    path = './analytics/ai_safety_log.jsonl'
    if not os.path.exists(path):
        return []
    entries = []
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                entry = eval(line.strip())
                if not user or entry.get('user') == user:
                    entries.append(entry)
            except Exception:
                continue
    entries = sorted(entries, key=lambda x: x.get('timestamp', ''), reverse=True)
    return entries[:limit]

@app.get("/admin/export-history")
def get_export_history(limit: int = Query(50, ge=1, le=1000), user: str = Query(None), current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Admin only")
    import os, json
    path = './logs/export_failures.json'
    if not os.path.exists(path):
        return []
    try:
        with open(path, 'r', encoding='utf-8') as f:
            entries = json.load(f)
        if user:
            entries = [e for e in entries if e.get('user') == user]
        entries = sorted(entries, key=lambda x: x.get('timestamp', ''), reverse=True)
        return entries[:limit]
    except Exception:
        return []

@app.get("/admin/users")
def get_users(current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Admin only")
    return STATIC_USERS_MEM

@app.post("/admin/users")
def add_user(user: dict = Body(...), current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Admin only")
    STATIC_USERS_MEM.append(user)
    return {"status": "ok", "users": STATIC_USERS_MEM}

@app.delete("/admin/users/{username}")
def delete_user(username: str, current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Admin only")
    global STATIC_USERS_MEM
    STATIC_USERS_MEM = [u for u in STATIC_USERS_MEM if u["username"] != username]
    return {"status": "ok", "users": STATIC_USERS_MEM}

from fastapi import Request
from backend.ai_prompt_engine.generate_vault import generate_vault_prompt
from backend.utils.monitoring import VaultMetrics
from backend.analytics.analytics_service import AnalyticsService

# --- Phase Control Panel State ---
from backend.phase_control_state import (
    load_state, save_state, update_phase, toggle_safe_mode, trigger_upgrade, lockdown_system
)

@app.get("/api/phase/status")
def get_phase_status(current_user: dict = Depends(get_current_user)):
    state = load_state()
    return {
        "phase": state["phase"],
        "safe_mode": state["safe_mode"],
        "last_upgrade": state["last_upgrade"],
        "next_upgrade": state["next_upgrade"],
        "system_integrity": state["system_integrity"],
        "lockdown": state["lockdown"]
    }

@app.post("/api/phase/trigger-upgrade")
def api_trigger_upgrade(current_user: dict = Depends(get_current_user)):
    trigger_upgrade()
    state = load_state()
    return {"success": True, "last_upgrade": state["last_upgrade"], "next_upgrade": state["next_upgrade"]}

@app.post("/api/phase/safe-mode")
def api_toggle_safe_mode(current_user: dict = Depends(get_current_user)):
    mode = toggle_safe_mode()
    return {"success": True, "safe_mode": mode}

@app.post("/api/phase/lockdown")
def api_lockdown(current_user: dict = Depends(get_current_user)):
    lockdown_system()
    state = load_state()
    return {"success": True, "lockdown": state["lockdown"], "system_integrity": state["system_integrity"]}

import redis

# Setup Redis and AnalyticsService
redis_client = redis.Redis(host="localhost", port=6379, db=1)
vault_metrics = VaultMetrics()
analytics_service = AnalyticsService(redis_client)

@app.post("/api/generate-vault")
async def api_generate_vault(request: Request, user: str = Depends(get_current_user)):
    data = await request.json()
    topic = data.get("topic")
    # Compliance & anti-sentience logging
    vault_metrics.track_user_metrics(user_id=user, action="generate_vault", context={"topic": topic})
    result = generate_vault_prompt(topic)
    return result

# --- API: Compliance/Ethics Activity Log (JWT-protected) ---
@app.get("/api/monitor/activity")
def api_monitor_activity(user: str = Depends(get_current_user)):
    # Simulate activity log from recent error/cache/user metrics
    errors = redis_client.lrange('error_metrics', -20, -1)
    cache = redis_client.lrange('cache_metrics', -20, -1)
    user_actions = redis_client.lrange('user_metrics', -20, -1)
    activity = [*errors, *cache, *user_actions]
    return [json.loads(a) for a in activity if a]

# --- API: Compliance/Ethics Metrics (JWT-protected) ---
@app.get("/api/monitor/metrics")
def api_monitor_metrics(user: str = Depends(get_current_user)):
    # Simulate compliance metrics from system, api, and rate limit metrics
    system = vault_metrics.get_system_metrics()
    api = vault_metrics.get_api_metrics()
    rate_limit = vault_metrics.get_rate_limit_metrics()
    return {"system": system, "api": api, "rate_limit": rate_limit}

# --- API: Analytics Metrics (JWT-protected) ---
@app.get("/api/analytics/metrics")
def api_analytics_metrics(user: str = Depends(get_current_user)):
    metrics = analytics_service.get_metrics()
    return metrics

# --- Simulators for Creative Dashboard Panels (JWT-protected) ---
from fastapi.responses import JSONResponse
import random
import time

@app.get("/api/sim/vault-drop-countdown")
def sim_vault_drop_countdown(user: str = Depends(get_current_user)):
    # Simulate next drop in 2h 14m, with rare glitch
    now = int(time.time())
    drop_in = 2*3600 + 14*60 - (now % (2*3600 + 14*60))
    hours = drop_in // 3600
    mins = (drop_in % 3600) // 60
    secs = drop_in % 60
    glitch = random.random() < 0.07
    return JSONResponse({
        "vault_name": random.choice(["AIFOLIO™ Pro", "Stealth Bundle", "Elite Creator", "Compliance Kit"]),
        "display": f"{hours:02}:{mins:02}:{secs:02}",
        "glitch": glitch,
        "glitch_message": "System sync..." if glitch else None,
        "drop_time": now + drop_in
    })

@app.get("/api/sim/sales-heatmap")
def sim_sales_heatmap(user: str = Depends(get_current_user)):
    # Simulate 40-60 points with muted intensities
    points = [{
        "x": random.randint(10, 310),
        "y": random.randint(10, 150),
        "intensity": round(random.uniform(0.2, 0.9), 2)
    } for _ in range(random.randint(40, 60))]
    return JSONResponse({"points": points})

@app.get("/api/sim/ai-log-visualizer")
def sim_ai_log_visualizer(user: str = Depends(get_current_user)):
    # Simulate 10-20 recent logs
    log_types = ["INFO_SIM", "WARNING_SIM", "ERROR_SIM"]
    logs = [{
        "log_id_sim": f"LOG{random.randint(10000,99999)}",
        "timestamp_sim": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time() - i*random.randint(10, 60))),
        "message": random.choice([
            "Vault generated.", "Compliance check passed.", "User triggered automation.", "Suspicious pattern detected.", "Memory usage normal.", "Rate limit hit.", "Manual review required.", "Ethics audit complete.", "Cache cleared.", "System health optimal."])
        , "status": random.choice(log_types) if random.random() < 0.3 else "INFO_SIM"
    } for i in range(random.randint(10, 20))]
    return JSONResponse({"logs": logs})

@app.get("/api/sim/compliance-risk-score")
def sim_compliance_risk_score(user: str = Depends(get_current_user)):
    # Simulate risk score 0-100 and description
    score = random.randint(2, 18) + random.randint(0, 8)
    level = "LOW" if score < 20 else "MEDIUM" if score < 45 else "HIGH"
    desc = {
        "LOW": "Risk level is low. Compliance pipeline optimal.",
        "MEDIUM": "Moderate risk. Review recent activity.",
        "HIGH": "Elevated risk detected. Immediate review advised."
    }[level]
    return JSONResponse({"score": score, "description": desc})

# --- Serve Frontend (React/Vue/Next) ---
app.mount("/static", StaticFiles(directory="frontend/dist", html=True), name="static")

@app.get("/", response_class=HTMLResponse)
def serve_index():
    with open("frontend/dist/index.html") as f:
        return HTMLResponse(f.read())
