import json

def test_getdata(client):
    client.get('/api/deldata')
    res = client.get('/api/getdata')
    data = json.loads(res.data)
    assert data['data'] == []
    submit_data = {"date":"010120001", "time":0}
    client.post("/api/submitdata", json=submit_data)
    res = client.get('/api/getdata')
    data = json.loads(res.data)
    assert data['data'] == [["010120001", 0]]