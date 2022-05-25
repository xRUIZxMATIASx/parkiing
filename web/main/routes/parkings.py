import json
import requests
from flask import Blueprint, render_template, request, url_for, current_app
from flask import flash
from flask_login import login_required
from main import admin_required
from main.forms.Sensors import CreateSensor
from main.forms.Sensors import SensorFilter
from werkzeug.utils import redirect


parkings = Blueprint('parkings', __name__, url_prefix='/')


@parkings.route('/parkings/search', methods=["POST", "GET"])
@login_required
def scan():


    return render_template('test.html')


@parkings.route('/parkings/search/<id>', methods=["POST", "GET"])
@login_required
def show_parking(id):
    auth = request.cookies['access_token']
    headers = {
        'content-type': "application/json",
        'authorization': "Bearer " + auth
    }

    url = str(current_app.config['API_URL']) + '/parking/' + str(id)
    r = requests.get(url=url, headers=headers, json={})
    parking = json.loads(r.text)


    return render_template('parking.html', parking=parking)
