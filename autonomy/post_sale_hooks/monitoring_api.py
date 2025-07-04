from fastapi import FastAPI, HTTPException, Depends, Response
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from autonomy.post_sale_hooks.monitoring import get_failed_hooks, replay_failed_hooks
from autonomy.post_sale_hooks.hook_metrics import hook_metrics
import os
import datetime

SECRET_KEY = os.environ.get("ADMIN_JWT_SECRET", "supersecret")
ALGORITHM = "HS256"

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/token")

def log_audit(action, user):
    log_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../analytics/audit.log'))
    with open(log_path, 'a') as f:
        f.write(f"{datetime.datetime.utcnow().isoformat()} | {user} | {action}\n")

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        role: str = payload.get("role", "viewer")
        if username is None:
            raise credentials_exception
        return {"username": username, "role": role}
    except JWTError:
        raise credentials_exception

@app.get("/api/failed_hooks")
def api_get_failed_hooks(user=Depends(get_current_user)):
    log_audit("view_failed_hooks", user["username"])
    return get_failed_hooks()

@app.post("/api/replay_failed_hooks")
def api_replay_failed_hooks(user=Depends(get_current_user)):
    if user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    log_audit("replay_failed_hooks", user["username"])
    try:
        replay_failed_hooks()
        return {"status": "replay triggered"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/audit_log")
def get_audit_log(user=Depends(get_current_user)):
    if user["role"] not in ("admin", "viewer"):
        raise HTTPException(status_code=403, detail="Not authorized")
    log_audit("view_audit_log", user["username"])
    log_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../analytics/audit.log'))
    if not os.path.exists(log_path):
        return Response(content="", media_type="text/plain")
    with open(log_path, 'r') as f:
        return Response(content=f.read(), media_type="text/plain")

@app.get("/api/metrics/post_sale_hooks")
def get_post_sale_hook_metrics(user=Depends(get_current_user)):
    """
    Returns aggregated metrics for all post-sale hooks for dashboard or ops.
    """
    return hook_metrics.get_metrics()
