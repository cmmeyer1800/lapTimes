import requests
import sys

def main():
    for arg in sys.argv:
        if arg == '--full':
            requests.post('http://localhost:5000/api/submit/time', json={"time":4210})
            requests.post('http://localhost:5000/api/submit/time', json={"time":10560})
            requests.post('http://localhost:5000/api/submit/time', json={"time":19960})
            requests.post('http://localhost:5000/api/submit/time', json={"time":25820})
        if arg == '--single':
            res = requests.post('http://localhost:5000/api/submit/time', json={"time":12960})
            if res.ok:
                print(res.text)

if __name__ == "__main__":
    main()