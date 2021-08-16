def test_signup_post(client):
    response = client.get('/signup')