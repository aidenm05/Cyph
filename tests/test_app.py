import sys
import os
import pytest

# Ensure the parent directory is in the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import app

@pytest.fixture
def client():
    """Fixture to set up a test client for the app."""
    with app.test_client() as client:
        yield client

def test_homepage(client):
    """Test if the homepage loads successfully."""
    response = client.get('/')
    assert response.status_code == 200  # Ensure status code is 200
