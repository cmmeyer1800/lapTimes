import os

def test_login(client):
    form = {'name': os.environ['USER'], 'password': os.environ['PASS']}
    client.post('/auth/login', data=form)
    res = client.get("/main/live")
    assert res.headers.get("Location") == "http://localhost/main/live"