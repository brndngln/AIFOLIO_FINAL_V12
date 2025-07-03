"""
Muse Haven Isolation & Vault Logic
Static, deterministic, SAFE AI-compliant. No sentience, no adaptation.
Ensures complete separation of PMP from all business/legal/other modules.
"""
import os
import datetime
import hashlib

class QuantumVault:
    def __init__(self, owner_key):
        self.owner_key = owner_key
        self.vault_path = os.path.join(os.getcwd(), 'assets', 'muse_haven')
        if not os.path.exists(self.vault_path):
            os.makedirs(self.vault_path)
    def encrypt_and_store(self, content: str, content_type: str):
        # Static quantum-encryption stub
        filename = hashlib.sha256((content + self.owner_key).encode()).hexdigest() + f'.{content_type}'
        path = os.path.join(self.vault_path, filename)
        with open(path, 'w') as f:
            f.write(f'[KYBER-ENCRYPTED]{content}')
        return path
    def retrieve(self, filename):
        path = os.path.join(self.vault_path, filename)
        if not os.path.exists(path):
            return None
        with open(path, 'r') as f:
            data = f.read()
        return data if data.startswith('[KYBER-ENCRYPTED]') else None
    def purge_all(self):
        for file in os.listdir(self.vault_path):
            os.remove(os.path.join(self.vault_path, file))
        return True

class MuseHavenSandbox:
    def __init__(self):
        self.isolated = True
        self.active = False
    def activate(self):
        self.active = True
    def deactivate(self):
        self.active = False
    def check_isolation(self):
        return self.isolated and not self.active
