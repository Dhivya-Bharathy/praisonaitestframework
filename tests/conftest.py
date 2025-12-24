"""
Pytest configuration for tests
"""

import pytest


@pytest.fixture
def sample_output():
    """Sample agent output for testing"""
    return "This is a sample agent response with some content"


@pytest.fixture
def sample_json_output():
    """Sample JSON output"""
    return '{"status": "success", "data": {"message": "test"}}'

