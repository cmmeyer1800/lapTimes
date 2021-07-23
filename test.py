import requests
import sys
import random

def main():
    for arg in sys.argv:
        if arg == '--full':
            num = 0
            for x in range(11):
                requests.post('http://localhost:5000/api/submit/time', json={"time":num})
                num += random.randint(7000, 14000)
        if arg == '--single':
            res = requests.post('http://localhost:5000/api/submit/time', json={"time":12960})
            if res.ok:
                print(res.text)

if __name__ == "__main__":
    main()