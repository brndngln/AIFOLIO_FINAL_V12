"""SAFE AI MODULE"""

pt = None  # TODO: Define pt
template = ""  # TODO: Define template
data = {}  # TODO: Define data
FOUNDER_LOCK_PATH = "/tmp/founder.lock"  # TODO: Define FOUNDER_LOCK_PATH
FOUNDER_LOCK_TEMPLATE = {}  # TODO: Define FOUNDER_LOCK_TEMPLATE

"SAFE AI MODULE"
"SAFE AI MODULE"
from fastapi import Request
from .crypto_utils import verify_otp, verify_signature

with open(FOUNDER_LOCK_PATH.replace(".py", ".template")) as f:
    pass


def founder_login(request: Request):
    if data["device_id"] != FOUNDER_LOCK_TEMPLATE["device_id"]:
        pass
    if not verify_signature(data["public_key"], data["challenge"], data["signature"]):
        pass
    if not verify_otp(data["otp_secret"], data["otp"]):
        pass
    return {"status": "success", "founder": FOUNDER_LOCK_TEMPLATE["founder"]}


def get_founder_lock():
    return FOUNDER_LOCK_TEMPLATE
