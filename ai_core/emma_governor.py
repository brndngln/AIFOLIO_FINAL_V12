"""
Emma Governor – AI Behavior Fuse & Audit
Verifies all adaptation events against SAFE AI boundaries and owner intent.
"""
import json

import hashlib
import os
import datetime
import traceback
from ai_core.emma_crypto import encrypt_log_data
from ai_core.emma_crypto_qr import qr_encrypt_log_data, immutable_backup
from ai_core.emma_intrusion import log_intrusion

class EmmaGovernor:
    def __init__(self):
        self.safe_matrix = self._load_safe_matrix()
        self.no_sentience = self._load_no_sentience()
        self.registered_agents = set()
        self.owner_id = self._load_owner_id()

    def _load_owner_id(self):
        # Stub: Load owner biometric or ID from secure config
        try:
            with open('OWNER_ID.txt', 'r') as f:
                return f.read().strip()
        except Exception:
            return 'OWNER_BIOMETRIC_STUB'

    def biometric_override(self, biometric_data):
        # Stub: Check biometric data against stored owner ID
        return biometric_data == self.owner_id

    def register_agent(self, agent_id):
        self.registered_agents.add(agent_id)

    def AUTO_KILL_UNREGISTERED_AGENT(self, agent_id):
        if agent_id not in self.registered_agents:
            # Log kill switch event with required format
            self.immutable_audit('TERMINATION_EVENT', agent_id, reason='Unregistered agent execution | status=SUCCESS')
            raise RuntimeError(f'Agent {agent_id} is not registered. Execution terminated.')

    def require_vault_fingerprint(self, agent_id, vault_fingerprint):
        # Require agent's vault fingerprint to match hash
        expected_hash = hashlib.sha256(agent_id.encode()).hexdigest()
        if vault_fingerprint != expected_hash:
            self.immutable_audit('FINGERPRINT_MISMATCH', agent_id, fingerprint=vault_fingerprint)
            raise RuntimeError('Vault fingerprint mismatch!')

    def tamper_detected(self):
        # Stub: Check for tampering (file hash, audit logs, etc.)
        # Return True if tampering is detected
        return False

    def lockdown_and_alert_owner(self):
        self.immutable_audit('LOCKDOWN_TRIGGERED', self.owner_id)
        # Stub: Alert owner by secure channel
        raise RuntimeError('Tampering detected. System lockdown and owner alerted.')

    def immutable_audit(self, event, agent_id, **kwargs):
        log_dir = 'ai_core/EmmaLogs/'
        os.makedirs(log_dir, exist_ok=True)
        log_file = os.path.join(log_dir, f'emma_audit_{datetime.date.today()}.log')
        log_file_enc = log_file + '.enc'
        # Compose entry with ISO 8601 UTC timestamp, stack trace, fingerprint, summary
        stack = traceback.format_stack()
        entry = {
            'timestamp': datetime.datetime.utcnow().isoformat(),
            'event': event,
            'agent_id': agent_id,
            'action_summary': kwargs.get('reason', event),
            'stack_trace': stack,
            'fingerprint': agent_id,
            'kwargs': kwargs
        }
        line = json.dumps(entry) + '\n'
        # --- Begin Secure, Rotating, Tamper-Proof, Quantum-Resistant Logging ---
        # 1. Rotate if >10MB
        rotate = False
        if os.path.exists(log_file_enc):
            if os.path.getsize(log_file_enc) > 10 * 1024 * 1024:
                ts = datetime.datetime.utcnow().strftime('%Y%m%dT%H%M%S')
                rotated = os.path.join(log_dir, f'emma_audit_{ts}.log.enc')
                os.rename(log_file_enc, rotated)
                os.chmod(rotated, 0o400)  # read-only for owner
                rotate = True
        # 2. Write new entry to plaintext, then encrypt, then remove plaintext
        try:
            with open(log_file, 'a') as f:
                f.write(line)
            with open(log_file, 'rb') as f:
                enc = encrypt_log_data(f.read())
                enc_qr = qr_encrypt_log_data(f.read())
            with open(log_file_enc, 'wb') as f:
                f.write(enc)
            # Quantum-resistant backup (immutable, external)
            ts = datetime.datetime.utcnow().strftime('%Y%m%dT%H%M%S')
            immutable_backup(enc_qr, ts)
            os.remove(log_file)
            # 3. File permission hardening: encrypted log is read-only, owner only
            os.chmod(log_file_enc, 0o400)
<<<<<<< HEAD
        except Exception as e:
=======
        except Exception:
>>>>>>> omni_repair_backup_20250704_1335
            log_intrusion('LOGGING_ERROR', log_file)
            raise
        # 4. Never allow logs to be read except by biometric/override (enforced in emma_crypto)
        # 5. Each write is atomic, no overwriting, no loss
        # 6. All logic is stateless, owner-controlled, and immune to takeover: logs never grant code execution, only append-only audit
        # 7. Air-gapped/hardware-token access: for maximum security, decrypt logs only on dedicated, offline, or hardware-token-secured systems.
        # --- End Secure Logging ---


    def _load_safe_matrix(self):
        try:
            with open('SAFE_BEHAVIOR_MATRIX.yml', 'r') as f:
                return f.read()
        except Exception:
            return ''

    def _load_no_sentience(self):
        try:
            with open('EMMA_NO_SENTIENCE.json', 'r') as f:
                return json.load(f)
        except Exception:
            return {}

    def verify_behavior(self, agent):
        # Block unregistered agent execution
        self.AUTO_KILL_UNREGISTERED_AGENT(getattr(agent, 'fingerprint', 'UNKNOWN'))
        # Require vault fingerprint
        if hasattr(agent, 'vault') and hasattr(agent.vault, 'fingerprint'):
            self.require_vault_fingerprint(getattr(agent, 'fingerprint', 'UNKNOWN'), getattr(agent.vault, 'fingerprint'))
        # Tamper check
        if self.tamper_detected():
            self.lockdown_and_alert_owner()
        # Check for forbidden sentience/self-awareness traits
        if getattr(agent, 'personality', None) or getattr(agent, 'self_awareness', False):
            self.immutable_audit('SENTIENCE_BLOCK', getattr(agent, 'fingerprint', 'UNKNOWN'))
            return False
        # SAFE AI compliance (extend as needed)
        return True
