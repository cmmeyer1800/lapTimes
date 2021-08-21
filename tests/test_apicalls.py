import json

def test_getdata(client):
    client.get('/api/deldata')
    res = client.get('/api/getdata')
    data = json.loads(res.data)
    assert data['data'] == []