from flask import Flask, render_template, request, redirect, make_response
from flask_caching import Cache
from flask_socketio import SocketIO, emit, send
from datetime import datetime
from firebase_admin import credentials, firestore, initialize_app
import json

app = Flask(__name__)
app.config.update(TESTING = True, HOST = '0.0.0.0')
app.config['SECRET_KEY'] = 'UnicornTabletCalculator'
socketio = SocketIO(app)

class Datastore():
    def __init__(self):
        self.client = None
        self.table_id = "laptime.lapTimes.data"
        self.data = []
        self.current_time = ''
        cred = credentials.Certificate('key.json')
        self.default_app = initialize_app(cred)
        self.firedb = firestore.client()
        self.data_sets = self.firedb.collection('lap_datasets')

    def send_to_db(self, dataset_name):
        date = self.data[0]['date']
        ints = [dataline['laptime'] for dataline in self.data]
        json_format = {'date': date, 'data':ints}
        self.data_sets.document(dataset_name).set(json_format)

    def delete_all_bq(self):
        query = "DELETE FROM `laptime.lapTimes.data` WHERE true;"
        self.client.query(query)

    def add_data(self, data):
        date = datetime.now().strftime("%m-%d-%y")
        self.data.append({'date':date, 'laptime':data})

    def formatted_data(self):
        output = []
        for idx in range(1, len(self.data)):
            output.append({'date':self.data[idx]['date'], 'lap_num':idx, 'lap_time':self.data[idx]['laptime']-self.data[idx-1]['laptime']})
            if idx > 1:
                output[idx-1]['difference'] = output[idx-1]['lap_time']-output[idx-2]['lap_time']
            else:
                output[idx-1]['difference'] = 0
        return output

    def formatted_fire_data(self, input_data):
        output = []
        times = input_data[0]
        date = input_data[1]
        for idx in range(1, len(times)):
            output.append({'date':date, 'lap_num':idx, 'lap_time':times[idx]-times[idx-1]})
            if idx > 1:
                output[idx-1]['difference'] = output[idx-1]['lap_time']-output[idx-2]['lap_time']
            else:
                output[idx-1]['difference'] = 0
        return output

db = Datastore()
    
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/live', methods=['GET', 'POST'])
def live():
    if request.method == 'GET':
        return render_template('live.html')
    elif request.method == 'POST':
        id = request.form.get('id')
        db.send_to_db(id)
        db.data = []
        return redirect(f'/history/{id}')
    else:
        return 'HTTP Method is not allowed'

@app.route('/history', methods=['GET'])
def history():
    docs=db.data_sets.stream()
    return render_template('history_index.html', docs=docs)

@app.route('/history/<id>', methods=['GET'])
def history_specific(id):
    docs = db.data_sets.stream()
    for doc in docs:
        if doc.id == id:
            input_data = (doc.get('data'), doc.get('date'))
            return render_template('history.html', data=db.formatted_fire_data(input_data), id=id)
    return 'Not found'

@app.route('/history/<id>/excel.csv', methods=['GET'])
def history_specific_excel(id):
    docs = db.data_sets.stream()
    for doc in docs:
        if doc.id == id:
            csv = ''
            input_data = (doc.get('data'), doc.get('date'))
            data=db.formatted_fire_data(input_data)
            for row in data:
                csv += f'{row["date"]}, {row["lap_num"]}, {row["lap_time"]}, {row["difference"]}\n'
            response = make_response(csv)
            cd = 'attachment; filename='+ id +'.csv'
            response.headers['Content-Disposition'] = cd 
            response.mimetype='text/csv'
            return response
    return 'Not found'

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