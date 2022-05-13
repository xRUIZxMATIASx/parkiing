import json
from flask import Blueprint, render_template
import flask_login
from flask_login import login_required
from main import admin_required
from flask import Blueprint, render_template, request, url_for, current_app
from main.resources.auth import LoggedUser
from sphinx.util import requests

config = Blueprint('config', __name__, url_prefix='/')


@config.route('/config')
@login_required
def index():
    if flask_login.current_user.admin:
        url = str(current_app.config['API_URL']) + str('/user/' + str(flask_login.current_user.id))
        r = requests.get(url=url)
        if json.loads(r.text)['parkingId'] == None:
            return render_template('setup.html', current_user=flask_login.current_user)
        else:
            # Aca debo traer de la api los datos del parking
            return render_template('config-parking.html', current_user=flask_login.current_user)
    else:
        # Aca debo traer los datos de usuario
        return render_template('config-user.html', current_user=flask_login.current_user)


"""
@config.route('/config-admin')
@login_required
@admin_required
def config_admin():
    return render_template('home.html', current_user=flask_login.current_user)

@config.route('/config-user')
@login_required
def config_user():
    return render_template('home.html', current_user=flask_login.current_user)
"""