"""Pytest configuration and fixtures."""

import sys
from pathlib import Path

import pytest

# Add backend to Python path for imports
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))


@pytest.fixture
def anyio_backend():
    """Use asyncio for async tests."""
    return "asyncio"
