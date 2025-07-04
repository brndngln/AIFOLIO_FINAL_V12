import unittest
from ai_core.audit import AuditDaemon
from ai_core.agent.agent_template import SafeAIAgent

class TestAuditDaemon(unittest.TestCase):
    def setUp(self):
        self.audit = AuditDaemon()
        self.agent = SafeAIAgent()

    def test_log_event(self):
        self.audit.log_event('learn', self.agent.fingerprint, 'data', 1)
        self.assertEqual(len(self.audit.log), 1)
        self.assertEqual(self.audit.log[0]['event'], 'learn')

    def test_check_drift(self):
        self.agent.drift = True
        with self.assertRaises(RuntimeError):
            self.audit.check_drift(self.agent)

if __name__ == '__main__':
    unittest.main()
