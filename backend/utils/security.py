"""
Ultimate Security Utilities for AIFOLIO/OMNIELITE Backend
Covers password policy, RBAC, MFA stub, device fingerprinting, API key validation, and token/session security.
"""
import re
import os
import time
import hmac
import hashlib
from typing import List, Dict, Callable
from fastapi import HTTPException, Request, status, Depends
from functools import wraps

# --- Password Policy ---
PASSWORD_MIN_LENGTH = 12
PASSWORD_COMPLEXITY_REGEX = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_+\-=\[\]{};':\",.<>/?]).+$"
PASSWORD_ROTATION_DAYS = 90  # Stub for future implementation

def validate_password_policy(password: str):
    if len(password) < PASSWORD_MIN_LENGTH:
        raise HTTPException(status_code=400, detail=f"Password must be at least {PASSWORD_MIN_LENGTH} characters.")
    if not re.match(PASSWORD_COMPLEXITY_REGEX, password):
        raise HTTPException(status_code=400, detail="Password must contain upper, lower, digit, and special char.")
    # TODO: Check password history for rotation
    return True

# --- MFA Integration Stub ---
def require_mfa(user: dict):
    # TODO: Integrate with TOTP/SMS/app-based MFA
    # Raise HTTPException if MFA fails
    pass

# --- RBAC Decorator ---
def require_role(roles: List[str]):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            user = kwargs.get('current_user') or kwargs.get('user')
            if not user or user.get('role') not in roles:
                raise HTTPException(status_code=403, detail="Insufficient privileges.")
            return func(*args, **kwargs)
        return wrapper
    return decorator

# --- API Key Validation ---
API_KEY_HEADER = "X-API-KEY"
VALID_API_KEYS = os.getenv("AIFOLIO_VALID_API_KEYS", "testkey123").split(",")

def require_api_key(request: Request):
    api_key = request.headers.get(API_KEY_HEADER)
    if not api_key or api_key not in VALID_API_KEYS:
        raise HTTPException(status_code=401, detail="Invalid or missing API key.")

# --- Device Fingerprinting Stub ---
def get_device_fingerprint(request: Request):
    # Example: Combine IP, User-Agent, Accept-Language
    ip = request.client.host
    ua = request.headers.get('user-agent', '')
    lang = request.headers.get('accept-language', '')
    raw = f"{ip}|{ua}|{lang}"
    return hashlib.sha256(raw.encode()).hexdigest()

# --- Token Reuse Detection Stub ---
USED_TOKENS = set()

def check_token_reuse(token: str):
    if token in USED_TOKENS:
        raise HTTPException(status_code=401, detail="Token reuse detected.")
    USED_TOKENS.add(token)

# --- Secure Cookie Settings ---
COOKIE_SETTINGS = {
    "httponly": True,
    "secure": True,
    "samesite": "strict"
}

# --- Bot/Burst Detection Stub ---
def detect_bot(request: Request):
    # TODO: Integrate with CAPTCHA or bot detection service
    pass

# --- API Versioning Helper ---
def get_api_version(request: Request) -> str:
    path = request.url.path
    if path.startswith("/v1/"): return "v1"
    if path.startswith("/v2/"): return "v2"
    return "unversioned"

# --- Output Sanitization ---
def sanitize_output(data):
    # TODO: Implement output allow-listing, escaping, and redaction
    return data

# --- Admin Endpoint Protection ---
def require_admin(func: Callable):
    @wraps(func)
    def wrapper(*args, **kwargs):
        user = kwargs.get('current_user') or kwargs.get('user')
        if not user or user.get('role') != 'admin':
            raise HTTPException(status_code=403, detail="Admin privileges required.")
        return func(*args, **kwargs)
    return wrapper
