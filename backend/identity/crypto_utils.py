# crypto_utils.py
# Utilities for digital signature, device fingerprint, OTP verification
import hashlib
import hmac
import base64
import time
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend

# Device fingerprint
def get_device_fingerprint(device_info):
    data = f"{device_info['uuid']}|{device_info['os']}|{device_info['browser']}"
    return hashlib.sha256(data.encode()).hexdigest()

# Digital signature verification
def verify_signature(public_key_pem, message, signature):
    public_key = serialization.load_pem_public_key(public_key_pem.encode(), backend=default_backend())
    try:
        public_key.verify(signature, message.encode(), padding.PKCS1v15(), hashes.SHA256())
        return True
    except Exception:
        return False

# OTP (TOTP) verification
def verify_otp(secret, otp, window=1):
    for offset in range(-window, window+1):
        if generate_otp(secret, time.time() + offset*30) == otp:
            return True
    return False

def generate_otp(secret, for_time=None):
    if for_time is None:
        for_time = time.time()
    intervals_no = int(for_time // 30)
    key = base64.b32decode(secret, True)
    msg = intervals_no.to_bytes(8, 'big')
    h = hmac.new(key, msg, hashlib.sha1).digest()
    o = h[19] & 15
    code = (int.from_bytes(h[o:o+4], 'big') & 0x7fffffff) % 1000000
    return str(code).zfill(6)
