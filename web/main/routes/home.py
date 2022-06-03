import json
from datetime import datetime
from flask import Blueprint, render_template
import flask_login
from flask_login import login_required
from flask import Blueprint, render_template, request, url_for, current_app, make_response
from main.resources.auth import LoggedUser
from sphinx.util import requests

home = Blueprint('index', __name__, url_prefix='/')


@home.route('/')
@home.route('/index', methods=['POST', 'GET'])
@login_required
def index():
    auth = request.cookies['access_token']
    headers = {
        'content-type': "application/json",
        'authorization': "Bearer " + auth
    }
    if flask_login.current_user.admin:
        if flask_login.current_user.parkingId != None:
            url = str(current_app.config['API_URL']) + '/parking/' + str(flask_login.current_user.parkingId)
            r = requests.get(url=url, headers=headers)
            qr = json.loads(r.text)['qr']
            space = json.loads(r.text)['space']

            url = str(current_app.config['API_URL']) + '/history/get-all-history/' + str(flask_login.current_user.parkingId)
            r = requests.get(url=url, headers=headers)
            clients = json.loads(r.text)['history']

            clients_list = list()

            for jsn in clients:
                jsn['i_timestamp'] = datetime.fromtimestamp(jsn['i_timestamp'])
                jsn['f_timestamp'] = datetime.fromtimestamp(jsn['f_timestamp'])
                clients_list.append(jsn['userId']['userId'])

            total_clients = len(list(set(clients_list)))
            total_sales = len(clients)
            return render_template('home.html',
                                   current_user=flask_login.current_user,
                                   qr=qr,
                                   total_sales=total_sales,
                                   total_clients=total_clients,
                                   space=space,
                                   clients=clients)
        else:
            return render_template('home.html',
                                   current_user=flask_login.current_user)
    else:
        if request.method == 'POST':
            location = request.form['location']
            url = str(current_app.config['API_URL']) + '/parkings/' + location + '&' + '5000'
            r = requests.get(url=url)
            parkings = json.loads(r.text)['parkings']
            resp = make_response(render_template('home-common.html', current_user=flask_login.current_user, parkings=parkings))
            resp.set_cookie('location', location)
            return resp
        location = request.cookies.get('location')
        if location != None:
            url = str(current_app.config['API_URL']) + '/parkings/' + location + '&' + '5000'
            r = requests.get(url=url)
            parkings = json.loads(r.text)['parkings']
            return render_template('home-common.html', current_user=flask_login.current_user, parkings=parkings)
        else:
            return render_template('capture-location.html', current_user=flask_login.current_user)

