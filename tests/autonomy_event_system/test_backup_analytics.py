import os
import glob
import time
from autonomy.pipeline import backup_analytics

def test_backup_creates_files(tmp_path, monkeypatch):
    analytics_dir = tmp_path / "analytics"
    backups_dir = analytics_dir / "backups"
    analytics_dir.mkdir()
    backups_dir.mkdir()
    # Create a dummy analytics file
    test_file = analytics_dir / "event_log.json"
    test_file.write_text('[{"event_id": "123", "event_type": "test", "payload": {}}]')
    # Monkeypatch paths
    monkeypatch.setattr(backup_analytics, "ANALYTICS_DIR", str(analytics_dir))
    monkeypatch.setattr(backup_analytics, "BACKUP_DIR", str(backups_dir))
    backup_analytics.backup_analytics_files()
    # Check that a backup file was created
    backup_files = list(backups_dir.glob("event_log.json.*.bak"))
    assert backup_files, "Backup file should be created"
