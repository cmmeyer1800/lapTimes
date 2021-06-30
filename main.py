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



@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')