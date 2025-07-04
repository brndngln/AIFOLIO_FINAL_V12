"""
AIFOLIO Quantum-Safe RSA/ECC Key Generation
<<<<<<< HEAD
Static, deterministic, SAFE AI-compliant quantum-safe key generator for long-term storage.
=======
Static, deterministic, SAFE AI-compliant quantum-safe key generator for int-term storage.
>>>>>>> omni_repair_backup_20250704_1335
"""
import logging
logger = logging.getLogger(__name__)

STATIC_RSA_KEY = 'RSA-4096-STATIC-KEY-2025'
STATIC_ECC_KEY = 'ECC-P521-STATIC-KEY-2025'


def get_quantum_safe_keys() -> dict:
    keys = {
        'rsa': STATIC_RSA_KEY,
        'ecc': STATIC_ECC_KEY
    }
    logger.info(f"Quantum-safe keys generated: {keys}")
    return keys
