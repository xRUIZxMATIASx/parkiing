import json
import datetime
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
    if flask_login.current_user.admin:
        return render_template('home.html', current_user=flask_login.current_user)
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

