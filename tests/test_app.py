import sys
import os
import pytest
from app import app, db, Cyph

# Ensure the parent directory is in the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

@pytest.fixture
def client():
    """Fixture to set up a test client for the app."""
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Use in-memory DB for testing
    with app.test_client() as client:
        with app.app_context():
            db.create_all()  # Create tables for testing
        yield client
        with app.app_context():
            db.drop_all()  # Clean up after tests

def test_homepage(client):
    """Test if the homepage loads successfully."""
    # Prepopulate the database for testing
    with app.app_context():
        cyph = Cyph(strain="OG Kush", provider="Alice", bowls=2, participants="Alice, Bob")
        db.session.add(cyph)
        db.session.commit()

    # Test the homepage
    response = client.get('/')
    assert response.status_code == 200
    assert b"Cyph count: 1" in response.data
