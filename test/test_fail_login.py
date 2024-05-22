import pytest
from login_flask import app as flask_app  

@pytest.fixture
def client():
    flask_app.config['TESTING'] = True
    with flask_app.test_client() as client:
        yield client

# Incorrect Password
def test_login_failure(client):
    # User didn't contain capital letter for the first letter
    data = {"username": "testuser", "password": "test!1" }

    # Make 5 POST requests to the login route with incorrect answers (5 attempts)
    for _ in range(5):
        response = client.post("/auth/login", data=data)
        assert response.status_code == 302

    # Check that the flashed message is correct
    # This allows the test to access session data, which is where Flask stores data between requests.
    with client.session_transaction() as session:
        flash_message = dict(session['_flashes'])['message']
        assert flash_message == "You tried 5 attempts. Please try again later."
        #In Flask, the flash function is used to store messages that can be retrieved on the next request to the server. 
        #These messages are stored in session['_flashes']. 
        #The dict function is used to convert this to a dictionary, and ['message'] is used to retrieve the message.

# Incorrect Username and Password
def test_login_failure_incorrect_username_password(client):
    # Incorrect username and password
    data = {"username": "Testuse", "password": "wrongpass!"}
    response = client.post("/auth/login", data=data)
    assert response.status_code == 302

# Blank Fields
def test_login_failure_blank_fields(client):
    # Username and password fields left blank
    data = {"username": "", "password": ""}
    response = client.post("/auth/login", data=data)
    assert response.status_code == 302

