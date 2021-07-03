from flask import Flask, render_template, request, redirect
from flask_caching import Cache
from google.cloud import bigquery
from datetime import datetime
import json

class Redis_Database():
    def __init__(self,cache):
        self.cache = cache
        self.key = 'lap_times'

    def add_to_cache(self, append_data):
        date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cur_data = self.cache.get(self.key)
        cur_data.append([date_time,append_data])
        status = self.cache.set(self.key, cur_data)
        if status == False:
            print("An error has occured inserting into the Redis")

    def get_from_cache(self):
        data = self.cache.get(self.key)
        return data

class BQ_Database:
    def __init__(self):
        self.client = bigquery.Client.from_service_account_json(r"/home/collin/code/python/lapTimes/testing-315021-0d231ce1adcd.json")

    def send_to_db(self, time):
        date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        query = "INSERT INTO `testing-315021.lapTimes.testing` (laptime, date_time) VALUES ("+ str(time) +", '"+ date_time +"');"
        result = self.client.query(query)
        if result.exception():
            print("An error has occured inserting into the bigquery")
            print(result.exception())
            return -1
        else:
            return 0

    def get_from_db(self):
        query = "SELECT * FROM `testing-315021.lapTimes.testing` LIMIT 100"
        result = self.client.query(query)
        data = []
        for x in result:
            row = []
            for y in x:
                row.append(y)
            data.append(row)
        return data

    def clear_all_data(self):
        query = "DELETE FROM `testing-315021.lapTimes.testing` WHERE true;"
        result = self.client.query(query)


app = Flask(__name__)
cache = Cache(app, config={
    'CACHE_TYPE':'redis',
    'CACHE_KEY_PREFIX':'server1',
    'CACHE_REDIS_HOST':'localhost',
    'CACHE_REDIS_PORT':'6379',
    'CACHE_REDIS_URL':'redis://localhost:6379'
})
bqdb = BQ_Database()
rdb = Redis_Database(cache)


@app.route('/api/submit/time', methods=['POST'])
def submit_data():
    data = request.json
    lap_time = data["time"]
    rdb.add_to_cache(lap_time)
    result = bqdb.send_to_db(lap_time)
    if result == 0:
        return 'success'
    elif result == -1:
        return 'An error has occured inserting into the database'

@app.route('/api/get/time', methods=['GET'])
def get_data_json_from_redis():
    data = rdb.get_from_cache()
    for row in data:
        row[0] = row[0].strftime("%Y-%m-%d %H:%M:%S")
    data = json.dumps({'data':data})
    return data

@app.route('/', methods=['GET'])
def index():
    data = rdb.get_from_cache()
    print(data)
    return render_template('index.html', data=data)