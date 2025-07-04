import os
<<<<<<< HEAD
import base64
=======
>>>>>>> omni_repair_backup_20250704_1335
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
try:
    from pqcrypto.kem.kyber512 import generate_keypair, encrypt, decrypt
    PQCRYPTO_AVAILABLE = True
except ImportError:
    PQCRYPTO_AVAILABLE = False
    def generate_keypair():
        raise ImportError("pqcrypto.kem.kyber512 not available: Quantum-resistant encryption is disabled. Install pqcrypto and ensure Kyber512 support on your platform.")
    def encrypt(pk, key):
        raise ImportError("pqcrypto.kem.kyber512 not available: Quantum-resistant encryption is disabled.")
    def decrypt(sk, ct):
        raise ImportError("pqcrypto.kem.kyber512 not available: Quantum-resistant encryption is disabled.")

from secretsharing import PlaintextToHexSecretSharer

"""
Quantum-resistant log encryption and multi-key sharding for Emma Governor OMNIELITE.
- Kyber512 KEM for quantum-safe key encapsulation (requires pqcrypto)
- Shamir's Secret Sharing for multi-key sharding (3-of-5)
- Robust keypair management and airgap/HSM compatibility
- If pqcrypto is not available, quantum functions will raise ImportError and log fallback status.

Integration notes:
- Use split_key/combine_key for multi-party AES key recovery (always available).
- Use qr_encrypt_log_data/qr_decrypt_log_data for quantum-resistant log backup (if pqcrypto available).
- For HSM/airgap, export shares or keypair to secure hardware/offline.
- For SIEM, send alerts on any ImportError or fallback event.
"""

KYBER_KEYPAIR_PATH = 'ai_core/EmmaLogs/kyber.keypair'

# --- Keypair Management ---
def load_or_create_kyber_keypair():
    if not PQCRYPTO_AVAILABLE:
        raise ImportError("pqcrypto.kem.kyber512 not available: Quantum-resistant encryption is disabled. Install pqcrypto and ensure Kyber512 support on your platform.")
    if not os.path.exists(KYBER_KEYPAIR_PATH):
        pk, sk = generate_keypair()
        with open(KYBER_KEYPAIR_PATH, 'wb') as f:
            f.write(pk + b'::' + sk)
    else:
        with open(KYBER_KEYPAIR_PATH, 'rb') as f:
            pk, sk = f.read().split(b'::')
    return pk, sk

if PQCRYPTO_AVAILABLE:
    pk, sk = load_or_create_kyber_keypair()
else:
    pk, sk = None, None

# --- Multi-key Sharding (Shamir's Secret Sharing) ---
def split_key(key: bytes, threshold=3, shares=5):
    """Split a 32-byte AES key into N shares, requiring M to reconstruct (default 3-of-5)."""
    hexkey = key.hex()
    return PlaintextToHexSecretSharer.split_secret(hexkey, threshold, shares)

def combine_key(shares):
    """Reconstruct AES key from shares."""
    hexkey = PlaintextToHexSecretSharer.recover_secret(shares)
    return bytes.fromhex(hexkey)

# --- Quantum-Resistant Encryption ---
def qr_encrypt_log_data(data: bytes) -> bytes:
    """Encrypt log data using Kyber KEM for quantum resistance. Raises ImportError if pqcrypto unavailable."""
    if not PQCRYPTO_AVAILABLE:
        raise ImportError("pqcrypto.kem.kyber512 not available: Quantum-resistant encryption is disabled. Install pqcrypto and ensure Kyber512 support on your platform.")
    backend = default_backend()
    iv = os.urandom(16)
    # Generate a random AES session key
    session_key = os.urandom(32)
    # Encrypt session key with Kyber public key
    ct, ss = encrypt(pk, session_key)
    cipher = Cipher(algorithms.AES(session_key), modes.CBC(iv), backend=backend)
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(data) + padder.finalize()
    encryptor = cipher.encryptor()
    encrypted = encryptor.update(padded_data) + encryptor.finalize()
    # Store: IV + Kyber ciphertext + encrypted log
    return iv + ct + encrypted


def qr_decrypt_log_data(enc_data: bytes, biometric=None, override=False) -> bytes:
    """Decrypt log data using Kyber KEM (requires biometric/override, raises ImportError if pqcrypto unavailable)."""
    if not PQCRYPTO_AVAILABLE:
        raise ImportError("pqcrypto.kem.kyber512 not available: Quantum-resistant decryption is disabled. Install pqcrypto and ensure Kyber512 support on your platform.")
    if not (biometric or override):
        raise PermissionError('Biometric or owner override required to decrypt logs.')
    backend = default_backend()
    iv = enc_data[:16]
    ct = enc_data[16:16+800]  # Kyber512 ciphertext is 800 bytes
    encrypted = enc_data[16+800:]
    # Decrypt session key with Kyber secret key
    session_key = decrypt(sk, ct)
    cipher = Cipher(algorithms.AES(session_key), modes.CBC(iv), backend=backend)
    decryptor = cipher.decryptor()
    padded = decryptor.update(encrypted) + decryptor.finalize()
    unpadder = padding.PKCS7(128).unpadder()
    return unpadder.update(padded) + unpadder.finalize()



# External immutable backup (write-only, append-only)
def immutable_backup(data: bytes, ts: str, backup_dir=None):
    """
    Write quantum-encrypted log data to an immutable, append-only backup.
    If backup_dir is None, use './ai_core/EmmaLogs/immutable_backup/'.
    On failure, print warning and (optionally) send SIEM alert.
    """
    if backup_dir is None:
        backup_dir = './ai_core/EmmaLogs/immutable_backup/'
    try:
        os.makedirs(backup_dir, exist_ok=True)
        path = os.path.join(backup_dir, f'emma_audit_{ts}.log.qr.enc')
        with open(path, 'ab') as f:
            f.write(data)
    except Exception as e:
        print(f"[OMNIELITE WARNING] Immutable backup failed: {e}")
        # Optionally send SIEM/webhook alert here
