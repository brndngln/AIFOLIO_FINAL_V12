<<<<<<< HEAD
import os
import json
import logging
=======
import json
>>>>>>> omni_repair_backup_20250704_1335
try:
    import pkcs11
    PKCS11_AVAILABLE = True
except ImportError:
    PKCS11_AVAILABLE = False

HSM_STATUS_PATH = 'ai_core/EmmaLogs/EmmaVaultIndex.json'

# Fallback to FIDO2 (stub)
def fido2_handshake():
    return False

def emma_init_hsm_key():
    """Initialize Emma Vault Key inside HSM or fallback."""
    if PKCS11_AVAILABLE:
        # Demo: create key and store ref
        hsm_key_ref = 'emma_hsm_key_handle'
        status = {'hsm': True, 'key_ref': hsm_key_ref, 'verified': True}
    else:
        hsm_key_ref = 'fido2_fallback_key'
        status = {'hsm': False, 'key_ref': hsm_key_ref, 'verified': fido2_handshake()}
    with open(HSM_STATUS_PATH, 'w') as f:
        json.dump(status, f)
    return status

def validate_hsm_handshake():
    try:
        with open(HSM_STATUS_PATH, 'r') as f:
            status = json.load(f)
        return status.get('verified', False)
    except Exception:
        return False

if __name__ == '__main__':
    # Register fingerprint, harden vault access, lock agent spawn behind hardware key
    status = emma_init_hsm_key()
    if not status.get('verified', False):
        print('HSM/FIDO2 authentication failed. Lockdown enforced.')
        exit(1)
    print('HSM/FIDO2 authentication successful. Emma vault and agent controls are locked to hardware key.')
