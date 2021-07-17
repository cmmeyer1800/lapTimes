from re import sub
from flask import Flask, render_template, request, redirect, jsonify
from flask_caching import Cache
from google.cloud import bigquery
from datetime import datetime
import json

app = Flask(__name__)

class Datastore():
    def __init__(self):
        self.client = bigquery.Client.from_service_account_json(r"/home/collin/code/python/lapTimes/testing-315021-0d231ce1adcd.json")
        self.table_id = "testing-315021.lapTimes.testing_data"
        self.data = []
        self.current_time = ''

    def send_to_bq(self):
        result = self.client.insert_rows_json(self.table_id, self.data)
        print(result)

    def delete_all_bq(self):
        query = "DELETE FROM `testing-315021.lapTimes.testing` WHERE true;"
        self.client.query(query)

    def add_data(self, data):
        time = datetime.now().strftime("%m-%d-%y %H:%M:%S")
        self.data.append({'datetime':time, 'laptime':   data})

db = Datastore()

@app.route('/')
def index():
    data = db.data
    return render_template('index.html', data=data)

@app.route('/_times', methods=['GET'])
def get_times():
    data = db.data
    return jsonify(data)

@app.route('/api/submit/time', methods=['POST'])
def add_data():
    time_data = request.get_json()['time']
    db.add_data(time_data)
    return 'success'

@app.route('/api/bq', methods=['GET'])
def test_send():
    db.send_to_bq()
    return 'success'

'''
query = "INSERT INTO `testing-315021.lapTimes.testing` (laptime, date_time) VALUES ("+ str(time) +", '"+ date_time +"');"

query = "SELECT * FROM `testing-315021.lapTimes.testing` LIMIT 100"

query = "DELETE FROM `testing-315021.lapTimes.testing` WHERE true;"

.strftime("%Y%m%d-%H%M%S")
'''