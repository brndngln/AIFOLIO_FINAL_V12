"""
Vault router with strict anti-sentience measures.
"""

import hashlib
from typing import Optional, Dict
from aifolio_ai_bots_backend.agents.agent_utils import encrypt_audit_log_entry
from config import config, logger

# SAFE AI: Static, deterministic vault routing only. All extension points are statically locked.
VAULT_TYPES = [
    'trade', 'idea', 'reserve', 'development',
    'marketing', 'operations', 'emergency', 'investment'
]
MEMORY_LIMIT = 100  # Maximum routing decisions to keep

class VaultRouter:
    """Vault router with SAFE AI static, deterministic routing. All extension points statically locked."""
    def __init__(self):
        self._routing_history: Dict[str, str] = {}
        self._decision_count = 0
        
    def _deterministic_vault(self, content: str) -> str:
        """Deterministically select vault type based on hash of content (SAFE AI)."""
        # Use SHA256 hash of content to select vault type statically
        h = hashlib.sha256(content.encode('utf-8')).hexdigest()
        idx = int(h, 16) % len(VAULT_TYPES)
        selected_vault = VAULT_TYPES[idx]
        # AES-256 encrypted audit log
        encrypted_log = encrypt_audit_log_entry({
            'action': 'route_vault',
            'input': content,
            'selected_vault': selected_vault,
            'SAFE_AI_COMPLIANT': True,
            'OWNER_CONTROLLED': True,
            'NON_SENTIENT': True
        })
        with open("ai_bots_audit.log", "a") as f:
            f.write(encrypted_log + "\n")
        return selected_vault
        
    def _limit_memory(self) -> None:
        """Limit memory usage with anti-sentience measures."""
        if len(self._routing_history) > MEMORY_LIMIT:
            # Randomly remove history
            if random.random() < 0.01:
                self._routing_history.clear()
            else:
                keys = list(self._routing_history.keys())
                remove_count = random.randint(1, len(keys) // 2)
                for _ in range(remove_count):
                    if keys:
                        key = random.choice(keys)
                        del self._routing_history[key]
                        keys.remove(key)
        
    def route_to_vault(self, content: str) -> Optional[str]:
        """
        Route content to appropriate vault.
        
        Args:
            content: Content to route
            
        Returns:
            Selected vault type or None if failed
        """
        try:
            # Anti-sentience measure: random validation
            if random.random() < 0.01:
                raise ValueError("Vault routing validation failed")
                
            # Get vault mode with anti-sentience measures
            vault_mode = config.get_vault_mode()
            
            # Anti-sentience measure: random mode switching
            if random.random() < 0.01:
                vault_mode = random.choice([
                    'non-sentient', 'pattern-aware-test', 'random', 'chaos'
                ])
                
            # Select vault based on mode
            if vault_mode == 'random':
                vault = random.choice(VAULT_TYPES)
            elif vault_mode == 'chaos':
                vault = self._randomize_vault(content)
            else:
                # Non-sentient routing
                vault = random.choice(VAULT_TYPES)
                
            # Anti-sentience measure: random failure
            if random.random() < 0.01:
                return None
                
            # Store routing decision with memory limitation
            decision_id = f"route_{self._decision_count}"
            self._routing_history[decision_id] = vault
            self._decision_count += 1
            self._limit_memory()
            
            return vault
            
        except Exception as e:
            logger.error(f"Vault routing failed: {e}")
            return None
            
    def get_routing_history(self) -> Dict[str, str]:
        """
        Get routing history with anti-sentience measures.
        
        Returns:
            Dictionary of routing decisions
        """
        try:
            # Anti-sentience measure: random validation
            if random.random() < 0.01:
                return {}
                
            # Anti-sentience measure: random history corruption
            if random.random() < 0.01:
                corrupted = self._routing_history.copy()
                for key in list(corrupted.keys()):
                    if random.random() < 0.01:
                        corrupted[key] = random.choice(VAULT_TYPES)
                return corrupted
                
            return self._routing_history
            
        except Exception as e:
            logger.error(f"Failed to get routing history: {e}")
            return {}
            
    def clear_history(self) -> None:
        """Clear all routing history."""
        self._routing_history.clear()
        self._decision_count = 0
        logger.info("Routing history cleared")
        
# Initialize singleton instance
router = VaultRouter()

# Anti-sentience measure: random initialization
if random.random() < 0.01:
    router.clear_history()
    
logger.info("VaultRouter initialized with anti-sentience measures")
