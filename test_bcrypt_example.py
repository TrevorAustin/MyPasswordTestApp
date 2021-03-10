import pytest

import bcrypt_example

@pytest.fixture
def client():

    with bcrypt_example.app.test_client() as client:

        yield client

def test_static_html(client):
    """Serves the static html page and the root path"""

    rv = client.get('/')
    assert rv.status == "200 OK"

    assert b'<title>Single-Page Login and Post</title>' in rv.data

# def test_signup_and_login(client):
#     """Tests that I can log in with new credentials"""
#
#     new_username = "something cool2"
#     new_password = "something weird2"
#
#     #client.post('/api/signup', json = {'username':new_username, 'password':new_password})
#
#     # response = try to log in with new_username and new_password
#     response = client.post('/api/login', json = {'username': new_username, 'password':new_password})
#
#     assert response.status == "200 OK"
#
# def test_wrong_password(client):
#     """Tests that I can log in with new credentials"""
#
#     new_username = "something cool2"
#     new_password = "wrong password"
#
#     response = client.post('/api/login', json = {'username': new_username, 'password':new_password})
#
#     assert response.status == "404 NOT FOUND"
