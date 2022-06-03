import json
from datetime import datetime
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
    r = requests.get(url=url, headers=headers, json={})
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

    # Obtener fecha de inicio
    url = str(current_app.config['API_URL']) + '/slots/get-user/' + str(flask_login.current_user.id)
    r = requests.get(url=url, headers=headers)
    i_timestamp = json.loads(r.text)['timestamp']

    # Eliminar usuario
    url = str(current_app.config['API_URL']) + '/slots/delete-user'
    r = requests.post(url=url, headers=headers, json=data)

    # Guardar en history
    url = str(current_app.config['API_URL']) + '/parking/' + str(id)
    r = requests.get(url=url, headers=headers, json={})
    parking = json.loads(r.text)
    price = parking['price']
    dt = datetime.now()
    f_timestamp = datetime.timestamp(dt)
    data = {
        "parkingId": int(id),
        "userId": int(flask_login.current_user.id),
        "i_timestamp": int(i_timestamp),
        "f_timestamp": int(f_timestamp),
        "price": int(price)
    }
    url = str(current_app.config['API_URL']) + '/history/save-history'
    r = requests.post(url=url, headers=headers, json=data)


    return make_response(redirect(url_for('parkings.show_checkout', id=id)))


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


@parkings.route('/parkings/show-checkout/<id>', methods=["POST", "GET"])
@login_required
def show_checkout(id):
    auth = request.cookies['access_token']
    headers = {
        'content-type': "application/json",
        'authorization': "Bearer " + auth
    }

    url = str(current_app.config['API_URL']) + '/history/get-last-history/' + str(id)
    r = requests.get(url=url, headers=headers, json={"userId": int(flask_login.current_user.id)})
    history = json.loads(r.text)
    i_timestamp = history['i_timestamp']
    f_timestamp = history['f_timestamp']
    price = history['price']

    # Calculo
    total_seconds = f_timestamp - i_timestamp
    total_hours = total_seconds / 3600

    total_hours = round(total_hours)
    total_price = total_hours*float(price)
    i_datetime = datetime.fromtimestamp(i_timestamp)
    f_datetime = datetime.fromtimestamp(f_timestamp)

    url = str(current_app.config['API_URL']) + '/parking/' + str(id)
    r = requests.get(url=url, headers=headers, json={})
    parking = json.loads(r.text)


    return render_template('checkout.html', price=price,
                           total_hours=total_hours,
                           total_price=total_price,
                           i_datetime=i_datetime,
                           f_datetime=f_datetime,
                           parking=parking)

