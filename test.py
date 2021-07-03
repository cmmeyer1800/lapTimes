import requests

res = requests.post('http://localhost:5000/api/submit/time', json={"time":12960})
if res.ok:
    print(res.text)
