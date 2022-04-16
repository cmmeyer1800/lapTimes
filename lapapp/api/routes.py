from flask import Blueprint, request
from flask_login import login_required
from .. import db
from ..models import Data
import datetime


api = Blueprint(
    "api",
    __name__,
)


@api.route("/submitdata", methods=["POST"])
def submitdata():
    data = request.get_json()
    date = data.get("date")
    time = data.get("time")
    if time == None:
        return {"error": "time required but not found"}
    if date == None:
        date = datetime.date.today().strftime("%d-%m-%Y")
    if len(date) != 10 or date[2] != "-" or date[5] != "-":
        return {"error": "date not properly formatted"}
    if type(date) != str or type(time) != str:
        return {"error": "date and time not in string format"}
    try:
        timenum = int(time)
    except:
        return {"error": "time conversion from string to int failed"}
    else:
        new_data = Data(date=date, time=time)
        db.session.add(new_data)
        db.session.commit()
        return {"success": "data submitted"}


@api.route("/getdata", methods=["GET"])
def getdata():
    all_data = Data.query.all()
    ret = {"data": [[x.id, x.date, x.time] for x in all_data]}
    return ret


@api.route("/getdataformatted", methods=["GET"])
def getdataformatted():
    all_data = Data.query.all()
    real_times = []
    for idx, val in enumerate(all_data):
        if idx == 0:
            real_times.append([val.id, val.date, val.time, "N/A"])
        else:
            real_times.append(
                [
                    val.id,
                    val.date,
                    val.time,
                    round((val.time - all_data[idx - 1].time), 6),
                ]
            )
    ret = {"data": real_times}
    return ret
    # all_data = [[0, data.date, data.time, 0] for data in Data.query.all()]
    # print(all_data)
    # ret = {"data": all_data}
    # return ret


@api.route("/deldata", methods=["GET"])
def deldata():
    Data.query.delete()
    db.session.commit()
    return "done"
