"""Test utilities for AIFOLIO."""
import pytest
import tempfile
from pathlib import Path

@pytest.fixture
def temp_dir():
    """Create temporary directory."""
    return Path(tempfile.mkdtemp())

@pytest.fixture
def sample_data():
    """Sample test data."""
    return {"test": "data"}
