import os
import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding

# AES-256 symmetric key (should be securely generated/stored in production)
EMMA_SYMM_KEY = os.environ.get('EMMA_SYMM_KEY') or base64.urlsafe_b64encode(os.urandom(32))


def encrypt_log_data(data: bytes) -> bytes:
    backend = default_backend()
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(EMMA_SYMM_KEY[:32]), modes.CBC(iv), backend=backend)
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(data) + padder.finalize()
    encryptor = cipher.encryptor()
    encrypted = encryptor.update(padded_data) + encryptor.finalize()
    return iv + encrypted  # prepend IV


def decrypt_log_data(enc_data: bytes, biometric=None, override=False) -> bytes:
    # Only allow with biometric or override
    if not (biometric == os.environ.get('EMMA_OWNER_ID') or override):
        raise PermissionError('Biometric or owner override required to decrypt logs.')
    backend = default_backend()
    iv = enc_data[:16]
    cipher = Cipher(algorithms.AES(EMMA_SYMM_KEY[:32]), modes.CBC(iv), backend=backend)
    decryptor = cipher.decryptor()
    padded = decryptor.update(enc_data[16:]) + decryptor.finalize()
    unpadder = padding.PKCS7(128).unpadder()
    return unpadder.update(padded) + unpadder.finalize()
