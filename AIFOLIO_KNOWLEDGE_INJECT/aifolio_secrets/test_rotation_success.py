import unittest
from unittest.mock import patch
import aifolio_secrets.rotate_secret as rotate_secret


class TestSecretRotation(unittest.TestCase):
    @patch(
        "aifolio_secrets.rotate_secret.rotate_secret_with_vault",
        return_value="new_secret",
    )
    @patch("aifolio_secrets.rotate_secret.expire_old_secret")
    @patch("aifolio_secrets.rotate_secret.log_rotation_event")
    def test_rotate_all_secrets_success(self, mock_log, mock_expire, mock_rotate):
        results = rotate_secret.rotate_all_secrets()
        for result in results:
            self.assertEqual(result["status"], "SUCCESS")
        self.assertEqual(mock_log.call_count, len(rotate_secret.SECRETS_LIST))


if __name__ == "__main__":
    unittest.main()
