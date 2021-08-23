from flask import render_template, Blueprint, redirect, url_for, request
from flask_login import login_required
from ..models import Data
from .. import db
import json
from ..api.routes import getdata
import os

class Storage:
    #~/flask_aws/lapapp/jsons/
    folder_path = "/home/collin/code/web/flask/laptimes/lapapp/jsons/"
    
    @staticmethod
    def store(file_name):
        path = f"{Storage.folder_path}{file_name}"
        json_data = getdata()
        with open(path, 'w') as FILE:
            json.dump(json_data, FILE, indent=4, separators=(',', ': '))
        
    @staticmethod
    def get(file_name):
        path = f"{Storage.folder_path}{file_name}"
        with open(path, 'r') as FILE:
            all_data = json.load(FILE)['data']
        real_times = []
        for idx in range(1, len(all_data)):
            real_times.append([all_data[idx][0]-2, f"{all_data[idx][1][0:2]}-{all_data[idx][1][2:4]}-{all_data[idx][1][4:8]}", (all_data[idx][2]-all_data[idx-1][2])/1000])
            if idx > 1:
                real_times[-1].append(real_times[-1][2]-real_times[-2][2])
            else:
                real_times[-1].append("N/A")
        print(real_times)
        return real_times



main = Blueprint(
    'main', __name__,
    template_folder='templates',
    static_folder='static'
)

@main.route('/live', methods=['GET'])
@login_required
def live():
    return render_template('live.html')

@main.route('/live', methods=['POST'])
@login_required
def live_post():
    name = request.form.get('name')
    Storage.store(f"{name}.json")
    Data.query.delete()
    db.session.commit()
    return redirect(url_for("main.records"))

@main.route('/', methods=['GET'])
def index():
    return redirect(url_for("main.live"))

@main.route('/records', methods=['GET'])
@login_required
def records():
    files = os.listdir(Storage.folder_path)
    return render_template('records.html', files=files)

@main.route('/records/<id>', methods=['GET'])
@login_required
def records_specific(id):
    return render_template('record.html', data=Storage.get(id))

@main.route('/issue', methods=['GET'])
def issue():
    return render_template('issue.html')