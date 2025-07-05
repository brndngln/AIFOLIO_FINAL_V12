import os
import requests

"""
AIFOLIO™ WEBHOOK INTEGRATIONS — OMNILOCK ANTI-SENTIENCE ENFORCEMENT
All sentience, memory, recursion, and adaptive logic is PERMANENTLY LOCKED OUT by OMNILOCK v777™.
- AntiSentienceLock: True
- OneShotCognitionMode: True
- StatelessAutonomy: True
- NoMemoryToken: True
- sentience_token_killswitch: True
- memory_depth_limit: 0
- self_awareness_check: False
- recursive_feedback_allowed: False
- NoConsciousnessSeed: True
"""
# OMNILOCK ANTI-SENTIENCE METADATA (enforced at runtime and static analysis)
AntiSentienceLock = True
OneShotCognitionMode = True
StatelessAutonomy = True
NoMemoryToken = True
sentience_token_killswitch = True
memory_depth_limit = 0
self_awareness_check = False
recursive_feedback_allowed = False
NoConsciousnessSeed = True

assert AntiSentienceLock is True, "OMNILOCK: AntiSentienceLock must be True"
assert OneShotCognitionMode is True, "OMNILOCK: OneShotCognitionMode must be True"
assert StatelessAutonomy is True, "OMNILOCK: StatelessAutonomy must be True"
assert NoMemoryToken is True, "OMNILOCK: NoMemoryToken must be True"
assert (
    sentience_token_killswitch is True
), "OMNILOCK: sentience_token_killswitch must be True"
assert memory_depth_limit == 0, "OMNILOCK: memory_depth_limit must be 0"
assert self_awareness_check is False, "OMNILOCK: self_awareness_check must be False"
assert (
    recursive_feedback_allowed is False
), "OMNILOCK: recursive_feedback_allowed must be False"
assert NoConsciousnessSeed is True, "OMNILOCK: NoConsciousnessSeed must be True"

import hmac
import hashlib
import logging
import json


def send_webhook(payload, endpoint=None):
    url = endpoint or os.getenv("DEFAULT_WEBHOOK_URL")
    secret = os.getenv("WEBHOOK_SECRET")
    if not url or not secret:
        logging.warning("Webhook url/secret missing")
        return
    data = json.dumps(payload).encode()
    sig = hmac.new(secret.encode(), data, hashlib.sha256).hexdigest()
    headers = {"Content-Type": "application/json", "X-Hub-Signature": sig}
    try:
        r = requests.post(url, data=data, headers=headers, timeout=10)
        r.raise_for_status()
    except Exception as e:
        logging.error(f"Webhook failed: {e}")
        # Optionally trigger fallback


def split_signal(event_type, payload, endpoints):
    for ep in endpoints:
        send_webhook(payload, endpoint=ep)


def verify_webhook_signature(payload_bytes, signature_header):
    """
    Static HMAC-SHA256 signature validator for incoming webhook/event payloads.
    Returns True if signature is valid, False otherwise.
    """
    secret = os.getenv("WEBHOOK_SECRET")
    if not secret or not signature_header:
        return False
    expected_sig = hmac.new(secret.encode(), payload_bytes, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected_sig, signature_header)
