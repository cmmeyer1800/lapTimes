import os

def test_login(client):
    form = {'name': os.environ['USER'], 'password': os.environ['PASS']}
    client.post('/login', data=form)
    assert login_manager.current_user.username == os.environ['USER']