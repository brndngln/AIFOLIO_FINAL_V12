"""
Pytest configuration and fixtures for AIFOLIO tests.
"""

import pytest
import tempfile
import shutil
from pathlib import Path
from unittest.mock import Mock, patch
import asyncio
import json

@pytest.fixture
def temp_dir():
    """Create a temporary directory for tests."""
    temp_path = Path(tempfile.mkdtemp())
    yield temp_path
    shutil.rmtree(temp_path)

@pytest.fixture
def mock_api_response():
    """Mock API response for testing."""
    return {
        "status": "success",
        "data": {"test": "data"},
        "message": "Test response"
    }

@pytest.fixture
def sample_config():
    """Sample configuration for testing."""
    return {
        "api_base_url": "https://api.test.com",
        "timeout": 30,
        "retries": 3,
        "debug": False
    }

@pytest.fixture
def mock_file_system(temp_dir):
    """Mock file system with test files."""
    test_files = {
        "test.py": "# Test Python file",
        "config.json": json.dumps({"test": True}),
        "data.txt": "Test data content"
    }
    
    for filename, content in test_files.items():
        file_path = temp_dir / filename
        with open(file_path, 'w') as f:
            f.write(content)
    
    return temp_dir

@pytest.fixture
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture
def mock_database():
    """Mock database connection for testing."""
    db_mock = Mock()
    db_mock.execute.return_value = Mock()
    db_mock.fetchall.return_value = []
    db_mock.fetchone.return_value = None
    return db_mock

@pytest.fixture(autouse=True)
def reset_environment():
    """Reset environment variables after each test."""
    import os
    original_env = os.environ.copy()
    yield
    os.environ.clear()
    os.environ.update(original_env)
