def test_http_response(client):
    response = client.get('/main/')
    assert response.status_code == 302
    response = client.get('/main/live')
    assert response.status_code == 302
    response = client.get('/main/records')
    assert response.status_code == 302
    response = client.get('/main/issue')
    assert response.status_code == 200