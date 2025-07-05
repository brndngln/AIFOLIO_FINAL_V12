import os
import unittest
from unittest.mock import patch
from autonomy.post_sale_hooks.store_backup_to_archive import store_backup_to_archive


class TestStoreBackupToArchive(unittest.TestCase):
    @patch("shutil.copy2")
    def test_archive_success(self, mock_copy):
        os.environ["ARCHIVE_PATH"] = "/tmp"
        with patch("os.path.exists", return_value=True):
            store_backup_to_archive("order1", "vault1")
        del os.environ["ARCHIVE_PATH"]

    def test_log_only(self):
        if "ARCHIVE_PATH" in os.environ:
            del os.environ["ARCHIVE_PATH"]
        with patch("os.path.exists", return_value=False):
            store_backup_to_archive("order2", "vault2")


if __name__ == "__main__":
    unittest.main()
