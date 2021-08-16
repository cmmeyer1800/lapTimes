from flask import render_template, Blueprint, redirect
from flask_login import login_required
from . import db

main = Blueprint('main', __name__)

@main.route('/live', methods=['GET'])
@login_required
def live():
    return render_template('live.html')

@main.route('/history', methods=['GET'])
def history():
    return render_template('history.html')

@main.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@main.route('/docs', methods=['GET'])
@login_required
def docs():
    return render_template('docs.html')
