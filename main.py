from re import sub
from flask import Flask, render_template, request, redirect
from flask_caching import Cache
from google.cloud import bigquery
from datetime import datetime
import json

app = Flask(__name__)

class Datastore():
    def __init__(self):
        self.client = bigquery.Client.from_service_account_json(r"/home/collin/code/python/lapTimes/testing-315021-0d231ce1adcd.json")
        self.cache = Cache(app, config={'CACHE_TYPE':'redis','CACHE_KEY_PREFIX':'server1',
        'CACHE_REDIS_HOST':'localhost','CACHE_REDIS_PORT':'6379','CACHE_REDIS_URL':'redis://localhost:6379'})
        self.time_key = 'lap_times'
        self.day_key = 'today'
        self.table_id = "testing-315021.lapTimes.testing_data"
    
    def get_from_db(self):
        self.check_today(datetime.datetime().strftime("%Y%m%d"))
        return self.cache.get(self.time_key)

    def post_to_db(self, data):
        self.check_today(datetime.now().strftime("%Y%m%d"))
        current_data = self.cache.get(self.time_key)
        current_data.append([datetime.datetime().strftime("%Y%m%d-%H%M%S"), data])
        self.cache.set(self.time_key, current_data)

    def check_today(self, submit_day):
        redis_day = self.cache.get(self.day_key)
        if not submit_day == redis_day:
            all_data_from_day = self.cache.get(self.time_key)
            formatted_data = []
            for row in all_data_from_day:
                formatted_data.append({"datetime":row[0], "laptime":[1]})
            self.client.insert_rows_json(self.table_id, formatted_data)
            self.cache.set(self.time_key, [])
            self.cache.set(self.day_key, submit_day)
        
db = Datastore()

'''
query = "INSERT INTO `testing-315021.lapTimes.testing` (laptime, date_time) VALUES ("+ str(time) +", '"+ date_time +"');"

query = "SELECT * FROM `testing-315021.lapTimes.testing` LIMIT 100"

query = "DELETE FROM `testing-315021.lapTimes.testing` WHERE true;"

.strftime("%Y%m%d-%H%M%S")

json.dumps({'data':data})

data = request.json
'''