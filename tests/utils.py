"""Test utilities and helpers.

This module provides common utilities and helpers for testing
across the entire test suite.
"""

import json
import tempfile
from pathlib import Path
from typing import Any, Dict, List
from unittest.mock import Mock, MagicMock
import pytest


class TestDataFactory:
    """Factory for creating test data."""
    
    @staticmethod
    def create_user_data(**kwargs) -> Dict[str, Any]:
        """Create test user data."""
        default_data = {
            "id": 1,
            "name": "Test User",
            "email": "test@example.com",
            "active": True
        }
        default_data.update(kwargs)
        return default_data
    
    @staticmethod
    def create_portfolio_data(**kwargs) -> Dict[str, Any]:
        """Create test portfolio data."""
        default_data = {
            "id": 1,
            "name": "Test Portfolio",
            "assets": ["AAPL", "GOOGL", "MSFT"],
            "total_value": 100000.0
        }
        default_data.update(kwargs)
        return default_data


class MockAPIClient:
    """Mock API client for testing."""
    
    def __init__(self):
        self.responses = {}
        self.call_history = []
    
    def set_response(self, endpoint: str, response: Any):
        """Set mock response for an endpoint."""
        self.responses[endpoint] = response
    
    def get(self, endpoint: str, **kwargs):
        """Mock GET request."""
        self.call_history.append(("GET", endpoint, kwargs))
        return self.responses.get(endpoint, {"status": "success"})
    
    def post(self, endpoint: str, data=None, **kwargs):
        """Mock POST request."""
        self.call_history.append(("POST", endpoint, data, kwargs))
        return self.responses.get(endpoint, {"id": 123, "status": "created"})


class TestFileManager:
    """Manages test files and directories."""
    
    def __init__(self):
        self.temp_dirs = []
        self.temp_files = []
    
    def create_temp_dir(self) -> Path:
        """Create a temporary directory."""
        temp_dir = Path(tempfile.mkdtemp())
        self.temp_dirs.append(temp_dir)
        return temp_dir
    
    def create_temp_file(self, content: str = "", suffix: str = ".txt") -> Path:
        """Create a temporary file."""
        temp_file = Path(tempfile.mktemp(suffix=suffix))
        temp_file.write_text(content)
        self.temp_files.append(temp_file)
        return temp_file
    
    def cleanup(self):
        """Clean up all temporary files and directories."""
        for temp_file in self.temp_files:
            if temp_file.exists():
                temp_file.unlink()
        
        for temp_dir in self.temp_dirs:
            if temp_dir.exists():
                import shutil
                shutil.rmtree(temp_dir)


def assert_json_equal(actual: str, expected: str):
    """Assert that two JSON strings are equal."""
    actual_data = json.loads(actual)
    expected_data = json.loads(expected)
    assert actual_data == expected_data


def assert_file_exists(file_path: Path):
    """Assert that a file exists."""
    assert file_path.exists(), f"File {file_path} does not exist"


def assert_directory_exists(dir_path: Path):
    """Assert that a directory exists."""
    assert dir_path.is_dir(), f"Directory {dir_path} does not exist"
