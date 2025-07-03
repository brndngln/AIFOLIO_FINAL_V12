import os
import time
import json
import threading
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding

LOG_PATH = '/opt/emma_logs/audit.log'
BUFFER_PATH = './ai_core/EmmaLogs/remote_buffer.log'
OWNER_FINGERPRINT = os.environ.get('EMMA_OWNER_ID', 'OWNER_BIOMETRIC_STUB')

class RemoteLogger:
    def __init__(self):
        self.buffer = []
        self.lock = threading.Lock()
        self.connected = False
        self._load_buffer()
        self._start_sync_thread()

    def _load_buffer(self):
        if os.path.exists(BUFFER_PATH):
            with open(BUFFER_PATH, 'r') as f:
                self.buffer = [json.loads(line) for line in f if line.strip()]

    def _save_buffer(self):
        with open(BUFFER_PATH, 'w') as f:
            for entry in self.buffer:
                f.write(json.dumps(entry) + '\n')

    def _start_sync_thread(self):
        t = threading.Thread(target=self._sync_loop, daemon=True)
        t.start()

    def _sync_loop(self):
        while True:
            if os.path.exists(os.path.dirname(LOG_PATH)):
                self.connected = True
                self.flush()
            else:
                self.connected = False
            time.sleep(10)

    def log(self, event_type, agent_id, context=None):
        entry = {
            'event_type': event_type,
            'agent_id': agent_id,
            'timestamp': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
            'context': context or {},
            'chain': self._chain_hash()
        }
        self.buffer.append(entry)
        self._save_buffer()
        if self.connected:
            self.flush()

    def flush(self):
        if not self.buffer:
            return
        with open(LOG_PATH, 'a') as f:
            for entry in self.buffer:
                f.write(self._encrypt_entry(entry))
        self.buffer = []
        self._save_buffer()

    def _encrypt_entry(self, entry):
        key = OWNER_FINGERPRINT.encode('utf-8').ljust(32, b'0')[:32]
        iv = os.urandom(16)
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        padder = padding.PKCS7(128).padder()
        data = json.dumps(entry).encode()
        padded = padder.update(data) + padder.finalize()
        encrypted = cipher.encryptor().update(padded) + cipher.encryptor().finalize()
        return (iv + encrypted).hex() + '\n'

    def _chain_hash(self):
        # Simple timestamp chain for demo
        if not self.buffer:
            return ''
        last = self.buffer[-1]
        return str(hash(json.dumps(last)))

# Usage: logger = RemoteLogger(); logger.log('KILL_SWITCH', 'agent123', {'reason':'test'})
