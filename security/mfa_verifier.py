import pyotp
import redis
import os
import json
from datetime import datetime

REDIS_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')
r = redis.from_url(REDIS_URL)
MFA_SECRET_PREFIX = 'aifolio:mfa:admin:'

# Store MFA secret for admin (encrypted outside this demo)
def set_admin_mfa_secret(admin_id, secret):
    r.set(f'{MFA_SECRET_PREFIX}{admin_id}', secret)

def get_admin_mfa_secret(admin_id):
    return r.get(f'{MFA_SECRET_PREFIX}{admin_id}')

def verify_mfa_token(admin_id, token):
    secret = get_admin_mfa_secret(admin_id)
    if not secret:
        return False
    totp = pyotp.TOTP(secret.decode())
    return totp.verify(token)
