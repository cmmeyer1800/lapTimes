from flask import Blueprint, request
from flask_login import login_required
from .. import db
from ..models import Data

api = Blueprint(
    'api', __name__,
)

@api.route("/submitdata", methods=["POST"])
def submitdata():
    data = request.get_json()
    date = data.get('date')
    time = data.get('time')
    if data == None or time == None:
        return {"error":"date and time attributes required but not found"}
    else:
        new_data = Data(date=date, time=time)
        db.session.add(new_data)
        db.session.commit()
        return {"success":"data submitted"}

@api.route("/getdata", methods=["GET"])
def getdata():
    all_data = Data.query.all()
    ret = {"data":[(x.date, x.time) for x in all_data]}
    return ret

@api.route("/getdataformatted", methods=["GET"])
def getdataformatted():
    all_data = Data.query.all()
    real_times = []
    for idx in range(1, len(all_data)):
        real_times.append([all_data[idx].id-2, f"{all_data[idx].date[0:2]}-{all_data[idx].date[2:4]}-{all_data[idx].date[4:8]}", (all_data[idx].time-all_data[idx-1].time)/1000])
    ret = {"data": real_times}
    return ret

@api.route("/deldata", methods=['GET'])
def deldata():
    Data.query.delete()
    db.session.commit()
    return "done"