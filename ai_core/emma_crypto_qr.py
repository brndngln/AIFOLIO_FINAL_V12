import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding

try:
    from pqcrypto.kem.kyber512 import generate_keypair, encrypt, decrypt

    PQCRYPTO_AVAILABLE = True
except ImportError:
    PQCRYPTO_AVAILABLE = False

    def generate_keypair() -> None:
        raise ImportError(
            "pqcrypto.kem.kyber512 not available: Quantum-resistant encryption is disabled. Install pqcrypto and ensure Kyber512 support on your platform."
        )

    def encrypt(pk: bytes, key: bytes) -> None:
        raise ImportError(
            "pqcrypto.kem.kyber512 not available: Quantum-resistant encryption is disabled."
        )

    def decrypt(sk: bytes, ct: bytes) -> None:
        raise ImportError(
            "pqcrypto.kem.kyber512 not available: Quantum-resistant encryption is disabled."
        )


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

KYBER_KEYPAIR_PATH = "ai_core/EmmaLogs/kyber.keypair"


# --- Keypair Management ---
from typing import Optional, Any, Tuple, List

def load_or_create_kyber_keypair() -> Tuple[bytes, bytes]:
    """
    Loads or creates a Kyber512 keypair for quantum-safe encryption.
    Returns:
        Tuple of (public_key, secret_key) as bytes.
    Raises:
        ImportError: If pqcrypto is not available.
    """
    if not PQCRYPTO_AVAILABLE:
        raise ImportError(
            "pqcrypto.kem.kyber512 not available: Quantum-resistant encryption is disabled. Install pqcrypto and ensure Kyber512 support on your platform."
        )
    if not os.path.exists(KYBER_KEYPAIR_PATH):
        pk, sk = generate_keypair()
        with open(KYBER_KEYPAIR_PATH, "wb") as f:
            f.write(pk + b"::" + sk)
    else:
        with open(KYBER_KEYPAIR_PATH, "rb") as f:
            pk, sk = f.read().split(b"::")
    return pk, sk


if PQCRYPTO_AVAILABLE:
    pk, sk = load_or_create_kyber_keypair()
else:
    pk = None  # type: ignore[assignment]
    sk = None  # type: ignore[assignment]


# --- Multi-key Sharding (Shamir's Secret Sharing) ---
def split_key(key: bytes, threshold: int = 3, shares: int = 5) -> List[str]:
    """
    Split a 32-byte AES key into N shares, requiring M to reconstruct (default 3-of-5).
    Args:
        key: The AES key as bytes.
        threshold: Minimum shares required to reconstruct.
        shares: Total number of shares to generate.
    Returns:
        List of hex-encoded shares as strings.
    """
    hexkey = key.hex()
    shares_list = PlaintextToHexSecretSharer.split_secret(hexkey, threshold, shares)
    return list(shares_list)

def combine_key(shares: List[str]) -> bytes:
    """
    Reconstruct AES key from shares.
    Args:
        shares: List of hex-encoded shares.
    Returns:
        The reconstructed AES key as bytes.
    """
    hexkey_raw = PlaintextToHexSecretSharer.recover_secret(shares)
    if isinstance(hexkey_raw, bytes):
        hexkey = hexkey_raw.decode()
    else:
        hexkey = str(hexkey_raw)
    return bytes.fromhex(hexkey)


# --- Quantum-Resistant Encryption ---
def qr_encrypt_log_data(data: bytes) -> bytes:
    """
    Encrypt log data using Kyber KEM for quantum resistance. Raises ImportError if pqcrypto unavailable.
    Args:
        data: Log data to encrypt (bytes).
    Returns:
        Encrypted bytes (IV + Kyber ciphertext + encrypted log).
    Raises:
        ImportError: If pqcrypto is not available.
    """
    if not PQCRYPTO_AVAILABLE:
        raise ImportError(
            "pqcrypto.kem.kyber512 not available: Quantum-resistant encryption is disabled. Install pqcrypto and ensure Kyber512 support on your platform."
        )
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
    result = iv + ct + encrypted
    from typing import cast
    return cast(bytes, result)


def qr_decrypt_log_data(enc_data: bytes, biometric: Optional[Any] = None, override: bool = False) -> bytes:
    """
    Decrypt log data using Kyber KEM (requires biometric/override, raises ImportError if pqcrypto unavailable).
    Args:
        enc_data: Encrypted log data (bytes).
        biometric: Optional biometric credential.
        override: Owner override flag.
    Returns:
        Decrypted log data (bytes).
    Raises:
        ImportError: If pqcrypto is not available.
        PermissionError: If neither biometric nor override is provided.
    """
    if not PQCRYPTO_AVAILABLE:
        raise ImportError(
            "pqcrypto.kem.kyber512 not available: Quantum-resistant decryption is disabled. Install pqcrypto and ensure Kyber512 support on your platform."
        )
    if not (biometric or override):
        raise PermissionError("Biometric or owner override required to decrypt logs.")
    backend = default_backend()
    iv = enc_data[:16]
    ct = enc_data[16 : 16 + 800]  # Kyber512 ciphertext is 800 bytes
    encrypted = enc_data[16 + 800 :]
    # Decrypt session key with Kyber secret key
    session_key = decrypt(sk, ct)
    cipher = Cipher(algorithms.AES(session_key), modes.CBC(iv), backend=backend)
    decryptor = cipher.decryptor()
    padded = decryptor.update(encrypted) + decryptor.finalize()
    unpadder = padding.PKCS7(128).unpadder()
    return unpadder.update(padded) + unpadder.finalize()


# External immutable backup (write-only, append-only)
def immutable_backup(data: bytes, ts: str, backup_dir: Optional[str] = None) -> None:
    """
    Write quantum-encrypted log data to an immutable, append-only backup.
    Args:
        data: Quantum-encrypted log data (bytes).
        ts: Timestamp string for the backup filename.
        backup_dir: Optional backup directory path.
    """
    if backup_dir is None:
        backup_dir = "./ai_core/EmmaLogs/immutable_backup/"
    try:
        os.makedirs(backup_dir, exist_ok=True)
        path = os.path.join(backup_dir, f"emma_audit_{ts}.log.qr.enc")
        with open(path, "ab") as f:
            f.write(data)
    except Exception as e:
        print(f"[OMNIELITE WARNING] Immutable backup failed: {e}")
        # Optionally send SIEM/webhook alert here
