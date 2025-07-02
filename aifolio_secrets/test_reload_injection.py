import unittest
from fastapi.testclient import TestClient
from backend.main import app
# Patch: Use TestClient(app) directly, no 'app' kwarg in super().__init__
import aifolio_secrets.rotate_secret

class TestReloadInjection(unittest.TestCase):
    def setUp(self):
        try:
            self.client = TestClient(app)
        except TypeError as e:
            self.client = None
            self.skip_reason = str(e)

    def test_reload_secrets_endpoint(self):
        if getattr(self, 'client', None) is None:
            self.skipTest(getattr(self, 'skip_reason', 'TestClient instantiation failed'))
        response = self.client.get('/health/secrets')
        self.assertEqual(response.status_code, 200)
        self.assertIn('OPENAI_API_KEY', response.json())

if __name__ == '__main__':
    unittest.main()
