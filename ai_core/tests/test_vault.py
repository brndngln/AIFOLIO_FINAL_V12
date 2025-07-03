import unittest
from ai_core.agent.agent_template import SafeAIAgent
from ai_core.vault import Vault

class TestVault(unittest.TestCase):
    def setUp(self):
        self.agent = SafeAIAgent()
        self.vault = Vault()
        self.agent.owner_lock = True

    def test_evolve_strategy(self):
        result = self.vault.evolve_strategy(self.agent, mutation='mutate_x')
        self.assertTrue(result)
        self.assertEqual(len(self.vault.evolution_log), 1)

    def test_owner_lock_blocks(self):
        self.agent.owner_lock = False
        with self.assertRaises(PermissionError):
            self.vault.evolve_strategy(self.agent, mutation='mutate_x')

if __name__ == '__main__':
    unittest.main()
