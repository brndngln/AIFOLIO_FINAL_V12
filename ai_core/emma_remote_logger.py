import os
import time
import json
import threading
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding

LOG_PATH = os.environ.get("EMMA_REMOTE_LOG_PATH", "/opt/emma_logs/audit.log")
BUFFER_PATH = "./ai_core/EmmaLogs/remote_buffer.log"
OWNER_FINGERPRINT = os.environ.get("EMMA_OWNER_ID", "OWNER_BIOMETRIC_STUB")


from typing import List, Dict, Any, Optional

class RemoteLogger:
    def __init__(self) -> None:
        """
        Initializes the RemoteLogger with buffer, lock, and sync thread.
        """
        self.buffer: List[Dict[str, Any]] = []
        self.lock = threading.Lock()
        self.connected: bool = False
        self._load_buffer()
        self._start_sync_thread()

    def _load_buffer(self) -> None:
        """
        Loads the buffer from the buffer file.
        """
        if os.path.exists(BUFFER_PATH):
            with open(BUFFER_PATH, "r") as f:
                self.buffer = [json.loads(line) for line in f if line.strip()]

    def _save_buffer(self) -> None:
        """
        Saves the buffer to the buffer file.
        """
        with open(BUFFER_PATH, "w") as f:
            for entry in self.buffer:
                f.write(json.dumps(entry) + "\n")

    def _start_sync_thread(self) -> None:
        """
        Starts the background sync thread.
        """
        t = threading.Thread(target=self._sync_loop, daemon=True)
        t.start()

    def _sync_loop(self) -> None:
        """
        Background sync loop for remote logging.
        """
        while True:
            if os.path.exists(os.path.dirname(LOG_PATH)):
                self.connected = True
                self.flush()
            else:
                self.connected = False
            time.sleep(10)

    def log(self, event_type: str, agent_id: str, context: Optional[Dict[str, Any]] = None) -> None:
        """
        Logs an event to the buffer and flushes if connected.
        Args:
            event_type: Type of the event.
            agent_id: Agent identifier.
            context: Additional event context.
        """
        entry: Dict[str, Any] = {
            "event_type": event_type,
            "agent_id": agent_id,
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "context": context or {},
            "chain": self._chain_hash(),
        }
        self.buffer.append(entry)
        self._save_buffer()
        if self.connected:
            self.flush()

    def flush(self) -> None:
        """
        Flushes the buffer to the remote log file.
        """
        if not self.buffer:
            return
        with open(LOG_PATH, "a") as f:
            for entry in self.buffer:
                f.write(self._encrypt_entry(entry))
        self.buffer = []
        self._save_buffer()

    def _encrypt_entry(self, entry: Dict[str, Any]) -> str:
        """
        Encrypts a log entry for secure storage.
        Args:
            entry: The log entry dictionary.
        Returns:
            Encrypted log entry as a hex string.
        """
        key = OWNER_FINGERPRINT.encode("utf-8").ljust(32, b"0")[:32]
        iv = os.urandom(16)
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        padder = padding.PKCS7(128).padder()
        data = json.dumps(entry).encode()
        padded = padder.update(data) + padder.finalize()
        encrypted = cipher.encryptor().update(padded) + cipher.encryptor().finalize()
        return (iv + encrypted).hex() + "\n"

    def _chain_hash(self) -> str:
        """
        Computes a simple timestamp chain hash for demo purposes.
        Returns:
            Hash string of the last buffer entry.
        """
        if not self.buffer:
            return ""
        last = self.buffer[-1]
        return str(hash(json.dumps(last)))


# Usage: logger = RemoteLogger(); logger.log('KILL_SWITCH', 'agent123', {'reason':'test'})
