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
    for idx in range(1, len(all_data)):
        real_times.append(
            [
                all_data[idx].id - 2,
                # f"{all_data[idx].date[0:2]}-{all_data[idx].date[2:4]}-{all_data[idx].date[4:8]}",
                all_data[idx].date,
                round((all_data[idx].time - all_data[idx - 1].time) / 1000, 6),
            ]
        )
        if idx > 1:
            real_times[-1].append(round(real_times[-1][2] - real_times[-2][2], 6))
        else:
            real_times[-1].append("N/A")
    ret = {"data": real_times}
    return ret


@api.route("/deldata", methods=["GET"])
def deldata():
    Data.query.delete()
    db.session.commit()
    return "done"
