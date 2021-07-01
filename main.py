from flask import Flask, render_template, request, redirect, flash
from google.cloud import bigquery
from datetime import datetime

app = Flask(__name__)

def send_to_db(time):
    date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    client = bigquery.Client.from_service_account_json(r"/home/collin/code/python/lapTimes/testing-315021-0d231ce1adcd.json")
    query = "INSERT INTO `testing-315021.lapTimes.testing` (laptime, date_time) VALUES ("+ str(time) +", '"+ date_time +"');"
    result = client.query(query)
    if result.exception():
        print("An error has occured inserting into the database")
        print(result.exception())
        return -1
    else:
        return 0

def get_from_db():
    client = bigquery.Client.from_service_account_json(r"/home/collin/code/python/lapTimes/testing-315021-0d231ce1adcd.json")
    query = "SELECT * FROM `testing-315021.lapTimes.testing` LIMIT 100"
    result = client.query(query)
    data = []
    for x in result:
        row = []
        for y in x:
            row.append(y)
        data.append(row)
    return data

@app.route('/api/submit/time', methods=['POST'])
def submit_data():
    data = request.json
    lap_time = data["time"]
    result = send_to_db(lap_time)
    if result == 0:
        return 'success'
    elif result == -1:
        return 'An error has occured inserting into the database'

@app.route('/', methods=['GET'])
def index():
    data = get_from_db()
    return render_template('index.html', data=data)