import os
import flask

def test_login(client):
    form = {'name': os.environ['USER'], 'password': os.environ['PASS']}
    client.post('/auth/login', data=form, follow_redirects=True)
    client.get('/auth/logout')
    assert flask.session.get("_user_id") == None