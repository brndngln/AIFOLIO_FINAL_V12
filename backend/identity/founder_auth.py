# founder_auth.py
# FastAPI endpoints for founder-only authentication and lock enforcement
from fastapi import APIRouter, Request, HTTPException
from .crypto_utils import verify_signature, verify_otp
import json
import os

router = APIRouter()

FOUNDER_LOCK_PATH = os.path.join(os.path.dirname(__file__), "../../founder.lock")

# Load founder.lock
with open(FOUNDER_LOCK_PATH.replace(".py", ".template")) as f:
    FOUNDER_LOCK_TEMPLATE = json.load(f)


@router.post("/founder/login")
def founder_login(request: Request):
    data = await request.json()
    # Device, signature, OTP checks
    if data["device_id"] != FOUNDER_LOCK_TEMPLATE["device_id"]:
        raise HTTPException(status_code=403, detail="Device mismatch")
    if not verify_signature(data["public_key"], data["challenge"], data["signature"]):
        raise HTTPException(status_code=403, detail="Signature invalid")
    if not verify_otp(data["otp_secret"], data["otp"]):
        raise HTTPException(status_code=403, detail="OTP invalid")
    return {"status": "success", "founder": FOUNDER_LOCK_TEMPLATE["founder"]}


@router.get("/founder/lock")
def get_founder_lock():
    return FOUNDER_LOCK_TEMPLATE
