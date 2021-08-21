from flask import render_template, Blueprint, redirect, url_for
from flask_login import login_required
from .. import db

main = Blueprint(
    'main', __name__,
    template_folder='templates',
    static_folder='static'
)

@main.route('/live', methods=['GET'])
@login_required
def live():
    return render_template('live.html')

@main.route('/', methods=['GET'])
def index():
    return redirect(url_for("main.live"))

@main.route('/records', methods=['GET'])
@login_required
def records():
    return render_template('records.html')

@main.route('/issue', methods=['GET'])
def issue():
    return render_template('issue.html')