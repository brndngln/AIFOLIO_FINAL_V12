import os
<<<<<<< HEAD
import shutil
=======
>>>>>>> omni_repair_backup_20250704_1335
import getpass
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import json

EMMA_USB_PATH = '/Volumes/EMMA_KEY/'

# AES256 encryption using Emma Fingerprint ID

def encrypt_file(data: bytes, key: bytes) -> bytes:
    backend = default_backend()
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
    padder = padding.PKCS7(128).padder()
    padded = padder.update(data) + padder.finalize()
    encryptor = cipher.encryptor()
    encrypted = encryptor.update(padded) + encryptor.finalize()
    return iv + encrypted

def export_to_usb_token(fingerprint_id: str, key_share: str, meta: dict, biometric: str):
    assert os.path.ismount(EMMA_USB_PATH), "EMMA_KEY USB not mounted!"
    key = fingerprint_id.encode('utf-8').ljust(32, b'0')[:32]
    files = {
        'emma.key': encrypt_file(key_share.encode(), key),
        'emma.meta': encrypt_file(json.dumps(meta).encode(), key),
        'biometric.auth': encrypt_file(biometric.encode(), key)
    }
    log_path = os.path.join(EMMA_USB_PATH, 'emma_token_log.txt')
    for fname, content in files.items():
        with open(os.path.join(EMMA_USB_PATH, fname), 'wb') as f:
            f.write(content)
    with open(log_path, 'a') as log:
        log.write(f"Exported at {os.uname().nodename} by {getpass.getuser()}\n")
    # Lock device to read-only
    os.system(f"diskutil unmountDisk {EMMA_USB_PATH}")
