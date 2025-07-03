from ai_core.vault import Vault
from ai_core.emma_governor import EmmaGovernor

governor = EmmaGovernor()

class VaultManager:
    def __init__(self):
        self.vaults = {}
    def create_vault(self):
        vault = Vault()
        self.vaults[vault.id] = vault
        return vault
    def load_vault(self, vault_id, agent):
        vault = self.vaults.get(vault_id)
        if not vault:
            raise ValueError('Vault not found')
        # Require Emma Governor verification before adaptation
        governor.require_vault_fingerprint(agent.fingerprint, vault.fingerprint)
        # Owner signature check (stub: always True)
        if getattr(agent, 'owner_lock', False) is not True:
            governor.immutable_audit('OWNER_SIGNATURE_MISSING', agent.fingerprint)
            raise RuntimeError('Owner signature missing')
        return vault
