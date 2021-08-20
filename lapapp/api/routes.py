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
    ret = {"data":[(f"{x.date[0:2]}-{x.date[2:4]}-{x.date[4:8]}", x.time/1000) for x in all_data]}
    return ret

@api.route("/deldata", methods=['GET'])
@login_required
def deldata():
    Data.query.delete()
    db.session.commit()
    return "done"