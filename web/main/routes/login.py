import ast
import json

import requests
from flask import Blueprint, render_template, make_response, url_for
from flask import current_app, flash
from flask_login import login_required, logout_user
from flask_login import login_user
from main.forms.login import Login
from main.resources.auth import LoggedUser
from werkzeug.utils import redirect

login = Blueprint('login', __name__, url_prefix='/')


@login.route('/', methods=['POST', 'GET'])
def index():
    form_login = Login()
    if form_login.validate_on_submit():
        url = str(current_app.config['API_URL']) + str('/auth/login')

        data = '{"email":"' + form_login.email.data + \
               '", "password":"' + form_login.password.data + '"}'

        r = requests.post(url=url, headers={'content-type': 'application/json'}, data=data)

        if r.status_code == 200:
            user_json = json.loads(r.text)
            logged_user = LoggedUser(
                id=user_json['id'],
                admin=user_json['admin']
            )
            login_user(logged_user)
            if ast.literal_eval(user_json['admin']) == True:
                req = make_response(redirect(url_for('index.index')))
                req.set_cookie('access_token', user_json['access_token'], httponly=True)
                return req
            else:
                req = make_response(redirect(url_for('index.index')))
                req.set_cookie('access_token', user_json['access_token'], httponly=True)
                return req
        else:
            flash("Credenciales desconocidas. Por favor intente nuevamente.", 'danger')
        return redirect(url_for('login.index'))

    web = current_app.config['WEB_URL']

    return render_template('login.html',
                           form_login=form_login,
                           web=web)

@login.route('/logout')
@login_required
def logout():
    req = make_response(redirect(url_for('login.index')))
    req.set_cookie('access_token', '', httponly=True)
    logout_user()
    return req
