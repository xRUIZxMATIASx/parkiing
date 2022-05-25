import json

import flask_login
import requests
from flask import Blueprint, render_template, request, url_for, current_app, make_response
from flask import flash
from flask_login import login_required
from main import admin_required
from werkzeug.utils import redirect


parkings = Blueprint('parkings', __name__, url_prefix='/')


@parkings.route('/parkings/search', methods=["POST", "GET"])
@login_required
def search():
    return render_template('parkings-search.html')

@parkings.route('/parkings/search/<id>/scan', methods=["POST", "GET"])
@login_required
def scan(id):
    auth = request.cookies['access_token']
    headers = {
        'content-type': "application/json",
        'authorization': "Bearer " + auth
    }
    initialized = None
    url = str(current_app.config['API_URL']) + '/slots/get-user/' + str(flask_login.current_user.id)
    r = requests.post(url=url, headers=headers, json={})
    if r.status_code == 403:
        initialized = False
        return render_template('parkings-scan.html', initialized=initialized)
    elif r.status_code == 201:
        initialized = True
        return render_template('parkings-scan.html', initialized=initialized)





@parkings.route('/parkings/search/<id>/start', methods=["POST", "GET"])
@login_required
def start(id):
    auth = request.cookies['access_token']
    headers = {
        'content-type': "application/json",
        'authorization': "Bearer " + auth
    }
    data = {
        "parkingId": int(id),
        "userId": int(flask_login.current_user.id)
    }

    url = str(current_app.config['API_URL']) + '/slots/add-user'
    r = requests.post(url=url, headers=headers, json=data)

    return make_response(redirect(url_for('parkings.show_parking', id=id)))

@parkings.route('/parkings/search/<id>/stop', methods=["POST", "GET"])
@login_required
def stop(id):
    auth = request.cookies['access_token']
    headers = {
        'content-type': "application/json",
        'authorization': "Bearer " + auth
    }
    data = {
        "parkingId": int(id),
        "userId": int(flask_login.current_user.id)
    }

    url = str(current_app.config['API_URL']) + '/slots/delete-user'
    r = requests.post(url=url, headers=headers, json=data)
    result = json.loads(r.text)
    return make_response(redirect(url_for('parkings.show_parking', id=id)))


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
    slots = parking['slots']['slots']
    avaible_slots = 0
    can_finish = False
    for slot in slots:
        if slot['state'] == 0:
            avaible_slots += 1
        if slot['userId'] == flask_login.current_user.id:
            can_finish = True

    return render_template('parking.html', parking=parking,
                           avaible_slots=avaible_slots,
                           can_finish=can_finish)
