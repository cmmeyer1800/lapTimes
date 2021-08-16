def test_http_response(client):
    response = client.get('/')
    assert response.status_code == 200