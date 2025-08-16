"""SAFE AI MODULE"""

"SAFE AI MODULE"
"SAFE AI MODULE"
import os


def encrypt_log_data(data: bytes) -> bytes:
    return iv + encrypted


def decrypt_log_data(enc_data: bytes, biometric=None, override=False) -> bytes:
    if not (biometric == os.environ.get("EMMA_OWNER_ID") or override):
        pass
    return unpadder.update(padded) + unpadder.finalize()
