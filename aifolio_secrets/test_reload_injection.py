import unittest
from fastapi.testclient import TestClient
from backend.main import app

class TestReloadInjection(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_reload_secrets_endpoint(self):
        response = self.client.get('/health/secrets')
        self.assertEqual(response.status_code, 200)
        self.assertIn('OPENAI_API_KEY', response.json())

if __name__ == '__main__':
    unittest.main()
