from flask import render_template, Blueprint, redirect, url_for, request, make_response
from flask_login import login_required
from werkzeug.utils import find_modules
from ..models import Data
from .. import db
import json
from ..api.routes import getdata, getdataformatted
import os
import boto3
from botocore.exceptions import ClientError


class Storage:
    # "/home/ubuntu/flask_aws/lapapp/jsons/"
    folder_path = "/home/collin/Code/lapTimes/lapapp/jsons/"

    @staticmethod
    def store(file_name):
        path = os.path.join(Storage.folder_path, file_name)
        json_data = getdata()
        with open(path, "w") as FILE:
            json.dump(json_data, FILE, indent=4, separators=(",", ": "))

    @staticmethod
    def get(file_name):
        path = f"{Storage.folder_path}{file_name}"
        with open(path, "r") as FILE:
            all_data = json.load(FILE)["data"]
        real_times = []
        for idx in range(1, len(all_data)):
            real_times.append(
                [
                    all_data[idx][0] - 2,
                    f"{all_data[idx][1][0:2]}-{all_data[idx][1][2:4]}-{all_data[idx][1][4:8]}",
                    round((all_data[idx][2] - all_data[idx - 1][2]) / 1000, 6),
                ]
            )
            if idx > 1:
                real_times[-1].append(round(real_times[-1][2] - real_times[-2][2], 6))
            else:
                real_times[-1].append("N/A")
        return real_times

    @staticmethod
    def send_to_s3():
        s3_client = boto3.client("s3")
        for file in os.listdir(Storage.folder_path):
            file_path = os.path.join(Storage.folder_path, file)
            try:
                s3_client.upload_file(
                    file_path, "motorsportlaptimesbackupstorage", file
                )
            except ClientError as e:
                print(e)
                return "failure, check logs"
        return "success"


main = Blueprint("main", __name__, template_folder="templates", static_folder="static")


@main.route("/live", methods=["GET"])
@login_required
def live():
    return render_template("live.html")


@main.route("/live", methods=["POST"])
@login_required
def live_post():
    name = request.form.get("name")
    Storage.store(f"{name}.json")
    Data.query.delete()
    db.session.commit()
    return redirect(url_for("main.records"))


@main.route("/", methods=["GET"])
def index():
    return redirect(url_for("main.live"))


@main.route("/records", methods=["GET"])
@login_required
def records():
    files = os.listdir(Storage.folder_path)
    return render_template("records.html", files=files)


@main.route("/records", methods=["POST"])
@login_required
def records_post():
    record_name = [x for x in request.form.lists()][0][0]
    os.remove(os.path.join(Storage.folder_path, record_name))
    return redirect(url_for("main.records"))


@main.route("/records/<id>", methods=["GET"])
@login_required
def records_specific(id):
    return render_template("record.html", data=Storage.get(id), title=id)


@main.route("/records/<id>", methods=["POST"])
@login_required
def records_specific_post(id):
    new_name = f"{request.form.get('name')}.json"
    os.rename(
        os.path.join(Storage.folder_path, id),
        os.path.join(Storage.folder_path, new_name),
    )
    return redirect(new_name)


@main.route("/records/<id>/excel.csv", methods=["GET"])
def records_specific_excel(id):
    csv = "id, date, time, difference\n"
    for row in Storage.get(id):
        csv += f"{row[0]},{row[1]},{row[2]},{row[3]}\n"
    response = make_response(csv)
    cd = "attachment; filename=" + id + ".csv"
    response.headers["Content-Disposition"] = cd
    response.mimetype = "text/csv"
    return response


@main.route("/issue", methods=["GET"])
def issue():
    return render_template("issue.html")


@main.route("/backup_data", methods=["GET"])
def backup():
    status = Storage.send_to_s3()
    return status
