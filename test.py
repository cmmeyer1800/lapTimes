import requests

res = requests.post('http://localhost:5000/api/submit/time', json={"time":12930})
if res.ok:
    print(res.text)
