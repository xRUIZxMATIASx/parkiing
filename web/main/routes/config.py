import json
from flask import Blueprint, render_template
import flask_login
from flask_login import login_required
from main import admin_required
from flask import Blueprint, render_template, request, url_for, current_app
from main.resources.auth import LoggedUser
from sphinx.util import requests
from werkzeug.utils import redirect
from main.forms.Parking import CreateParking

config = Blueprint('config', __name__, url_prefix='/')


@config.route('/config', methods=['POST', 'GET'])
@login_required
def index():
    if flask_login.current_user.admin:
        try:
            form_setup = CreateParking()
            if form_setup.validate_on_submit():
                print("Enviado")
                url = str(current_app.config['API_URL']) + str('/user/' + str(flask_login.current_user.id))
                r = requests.post(url=url)
                return redirect(url_for('index.index'))
            return render_template('setup.html', current_user=flask_login.current_user, form_setup=form_setup)
        except Exception as e:
            print(e)
    else:
        # Aca debo traer los datos de usuario
        return render_template('config-user.html', current_user=flask_login.current_user)


"""
@config.route('/config', methods=['POST', 'GET'])
@login_required
def index():
    if flask_login.current_user.admin:
        url = str(current_app.config['API_URL']) + str('/user/' + str(flask_login.current_user.id))
        r = requests.get(url=url)
        try:
            if json.loads(r.text)['parkingId'] == None: # Esto deberia quitarlo
                form_setup = CreateParking()
                if form_setup.validate_on_submit():
                    print("Enviado")
                    return redirect(url_for('index.index'))
                try:
                    return render_template('setup.html', current_user=flask_login.current_user, form_setup=form_setup)
                except Exception as e:
                    pass
            else:
                # Aca debo traer de la api los datos del parking
                return render_template('config-parking.html', current_user=flask_login.current_user)
        except Exception as e:
            print(e)
    else:
        # Aca debo traer los datos de usuario
        return render_template('config-user.html', current_user=flask_login.current_user)
"""