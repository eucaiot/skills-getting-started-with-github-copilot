"""Pytest configuration and shared fixtures for FastAPI tests."""

import pytest
from fastapi.testclient import TestClient
from src.app import app


@pytest.fixture
def client():
    """Fixture that provides a TestClient for making requests to the FastAPI app.
    
    Yields a TestClient instance that can be used in tests to make synchronous
    HTTP requests to the application endpoints.
    """
    with TestClient(app) as test_client:
        yield test_client
