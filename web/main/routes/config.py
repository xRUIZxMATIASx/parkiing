import json
from flask import Blueprint, render_template
import flask_login
from flask_login import login_required
from main import admin_required
from flask import Blueprint, render_template, request, url_for, current_app
from main.resources.auth import LoggedUser
import requests
from werkzeug.utils import redirect
from main.forms.Parking import CreateParking

config = Blueprint('config', __name__, url_prefix='/')


@config.route('/config', methods=['POST', 'GET'])
@login_required
def index():
    if flask_login.current_user.admin:
        auth = request.cookies['access_token']
        headers = {
            'content-type': "application/json",
            'authorization': "Bearer " + auth
        }
        url = str(current_app.config['API_URL']) + str('/user/' + str(flask_login.current_user.id))
        r = requests.get(url=url)
        try:
            form_setup = CreateParking()
            if json.loads(r.text)['parkingId'] == None:
                if form_setup.validate_on_submit():
                    url = str(current_app.config['API_URL']) + str('/parking/add')
                    data = {
                        "name": form_setup.name.data,
                        "location": form_setup.location.data,
                        "space": form_setup.space.data,
                        "price": form_setup.price.data,
                        "rate": 0,
                        "config": "",
                        "userId": flask_login.current_user.id
                    }
                    r = requests.post(url=url, headers=headers, json=data)
                    parkingId = json.loads(r.text)["parkingId"]
                    url = str(current_app.config['API_URL']) + str('/generateqr/' + str(parkingId))
                    requests.get(url=url, headers=headers)
                    data = {
                        "parkingId": parkingId
                    }
                    requests.put(current_app.config['API_URL'] + "/user/" + str(flask_login.current_user.id), headers=headers, data=json.dumps(data))
                    return redirect(url_for('index.index'))
                return render_template('setup.html', current_user=flask_login.current_user, form_setup=form_setup)
            else:
                r = requests.get(current_app.config['API_URL'] + "/parking/" + str(json.loads(r.text)['parkingId']), headers=headers)
                form_setup.name.data = json.loads(r.text)['name']
                form_setup.location.data = json.loads(r.text)['location']
                form_setup.space.data = json.loads(r.text)['space']
                form_setup.price.data = json.loads(r.text)['price']
                # Verificar si guardado los cambios
                return render_template('setup.html', current_user=flask_login.current_user, form_setup=form_setup)
        except Exception as e:
            print(e)
    else:
        # Aca debo traer los datos de usuario
        return render_template('config-user.html', current_user=flask_login.current_user)

