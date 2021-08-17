import os

def test_login(client):
    form = {'name': os.environ['USER'], 'password': os.environ['PASS']}
    response = client.post('/login', data=form)
    assert response.headers['Location'] != 'http://localhost/login'
