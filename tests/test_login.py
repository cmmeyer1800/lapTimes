import os
import flask

def test_login(client):
    form = {'name': os.environ['USER'], 'password': os.environ['PASS']}
    client.post('/auth/login', data=form, follow_redirects=True)
    assert flask.session['_user_id'] == '1'