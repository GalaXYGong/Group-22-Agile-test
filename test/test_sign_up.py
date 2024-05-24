import pytest
from login_flask import app as flask_app  

@pytest.fixture
def client():
    flask_app.config['TESTING'] = True
    with flask_app.test_client() as client:
        yield client

def test_register(client):
    # Register a new user as a test user
    data = {
        "username": "testuser12", 
        "password": "Test!1", 
        "secure_question1": "What is your favorite color?", 
        "answer1": "Blue", "secure_question2": 
        "What is your favorite food?", 
        "answer2": "Pizza"
        }
    response = client.post("/auth/register", data=data)  
    assert response.status_code == 302
    

def test_login(client):
    # Login with the test user
    data = {"username": "testuser12", "password": "Test!1"}
    response = client.post("/auth/login", data=data) 
    assert response.status_code == 302
   
    
def test_change_password(client):
    # Login with the test user
    login_data = {"username": "testuser12", "password": "Test!1"}
    client.post("/auth/login", data=login_data)  

    # Change password for the test user in the profile page
    new_password_data = {"password": "Test!1", "new_password": "Newtestpass!1"}
    response = client.post("/profile/update/password", data=new_password_data)
    assert response.status_code == 302  
    
