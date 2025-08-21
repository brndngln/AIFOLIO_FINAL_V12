"""Pytest configuration and fixtures.

This file contains shared pytest fixtures and configuration
for the entire test suite.
"""

import pytest
import tempfile
import shutil
from pathlib import Path
from unittest.mock import Mock


@pytest.fixture
def temp_dir():
    """Create a temporary directory for tests."""
    temp_path = Path(tempfile.mkdtemp())
    yield temp_path
    shutil.rmtree(temp_path)


@pytest.fixture
def mock_config():
    """Mock configuration object."""
    config = Mock()
    config.get = Mock(return_value="test_value")
    return config


@pytest.fixture
def sample_data():
    """Sample test data."""
    return {
        "test_key": "test_value",
        "numbers": [1, 2, 3, 4, 5],
        "nested": {
            "inner_key": "inner_value"
        }
    }


@pytest.fixture(scope="session")
def test_database():
    """Test database fixture."""
    # Setup test database
    yield "test_db"
    # Cleanup test database


@pytest.fixture
def mock_api_client():
    """Mock API client for testing."""
    client = Mock()
    client.get = Mock(return_value={"status": "success"})
    client.post = Mock(return_value={"id": 123})
    return client
