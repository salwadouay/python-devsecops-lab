# test_app.py (place this in the root of your project)
import pytest
from app import app # Assuming your Flask app instance is named 'app'

# Fixture to create a test client
@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home_route(client):
    # Sends a GET request to the '/' route
    response = client.get('/')
    # Asserts that the HTTP status code is 200 (OK)
    assert response.status_code == 200
    # Asserts that the response data contains the correct JSON message
    assert b'Hello, Flask!' in response.data
