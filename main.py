from flask import Flask, render_template, request, redirect, jsonify
from flask_caching import Cache
from flask_socketio import SocketIO, emit, send
from google.cloud import bigquery
from datetime import datetime
import json

app = Flask(__name__)
app.config.update(TESTING = True, HOST = '0.0.0.0')
app.config['SECRET_KEY'] = 'UnicornTabletCalculator'
socketio = SocketIO(app)

class Datastore():
    def __init__(self):
        self.client = bigquery.Client.from_service_account_json(r"/home/collin/code/python/lapTimes/laptime-dc30bfad5679.json")
        self.table_id = "laptime.lapTimes.data"
        self.data = []
        self.current_time = ''

    def __iter__(self):
        return (x for x in self.data)

    def send_to_bq(self):
        formattedData = [{'json':self.data}]
        result = self.client.insert_rows_json(self.table_id, formattedData)
        print(result)

    def delete_all_bq(self):
        query = "DELETE FROM `laptime.lapTimes.data` WHERE true;"
        self.client.query(query)

    def add_data(self, data):
        time = datetime.now().strftime("%m-%d-%y %H:%M:%S")
        self.data.append({'datetime':time, 'laptime':data})

    def formatted_data(self):
        output = []
        for idx in range(1, len(self.data)):
            output.append({'date':self.data[idx]['datetime'][0:8], 'lap_num':idx, 'lap_time':self.data[idx]['laptime']-self.data[idx-1]['laptime']})
            if idx > 1:
                output[idx-1]['difference'] = output[idx-1]['lap_time']-output[idx-2]['lap_time']
            else:
                output[idx-1]['difference'] = 0
        return output

db = Datastore()
    
@app.route('/', methods=['GET'])
def index():
    return redirect('live')

@app.route('/live', methods=['GET', 'POST'])
def live():
    if request.method == 'GET':
        return render_template('live.html')
    elif request.method == 'POST':
        pass
        # Process POST
    else:
        return 'Method is not allowed'

@app.route('/history/<id>', methods=['GET'])
def history(id):
    return str(id)

@app.route('/api/submit/time', methods=['POST'])
def add_data():
    time_data = request.get_json()['time']
    db.add_data(time_data)
    if len(db.formatted_data()) > 0:
        socketio.emit('add_data', json.dumps([db.formatted_data()[-1]]), json=True)
    return 'success'

@socketio.on('connect')
def connect():
    emit('add_data', json.dumps(db.formatted_data()), json=True)

if __name__ == "__main__":
    socketio.run(app)

'''
.strftime("%Y%m%d-%H%M%S")
'''