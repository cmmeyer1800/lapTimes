def test_http_response(client):
    response = client.get('/main')
    assert response.status_code == 200