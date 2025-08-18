"""Basic tests to verify test infrastructure works."""

import pytest
import sys
from pathlib import Path


def test_basic_functionality():
    """Test basic Python functionality."""
    assert 1 + 1 == 2
    assert "hello" == "hello"
    assert [1, 2, 3] == [1, 2, 3]


def test_project_structure(project_root_path):
    """Test that project structure is accessible."""
    assert project_root_path.exists()
    assert project_root_path.is_dir()


def test_sample_data(sample_data):
    """Test sample data fixture."""
    assert sample_data["test_value"] == 42
    assert sample_data["test_string"] == "hello world"
    assert sample_data["test_list"] == [1, 2, 3]


def test_imports():
    """Test that basic imports work."""
    import json
    import os
    import sys
    
    assert json is not None
    assert os is not None
    assert sys is not None


class TestBasicClass:
    """Test class for pytest class-based tests."""
    
    def test_class_method(self):
        """Test class-based test method."""
        assert True
    
    def test_class_with_fixture(self, sample_data):
        """Test class method with fixture."""
        assert sample_data is not None
