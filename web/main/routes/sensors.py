import json
import requests
from flask import Blueprint, render_template, request, url_for, current_app
from flask import flash
from flask_login import login_required
from main import admin_required
from main.forms.Sensors import CreateSensor
from main.forms.Sensors import SensorFilter
from werkzeug.utils import redirect

modify_sensor = Blueprint('modify_sensor', __name__, url_prefix='/')

sensors = Blueprint('sensors', __name__, url_prefix='/')


@sensors.route('/sensores')
@login_required
def index():
    auth = request.cookies['access_token']
    headers = {
        'content-type': "application/json",
        'authorization': "Bearer " + auth
    }

    form = SensorFilter(request.args, meta={'csrf': False})

    data = {}

    if 'name' in request.args and request.args['name'] != "":
        data["name"] = request.args.get('name', '')

    if 'status' in request.args and request.args['status'] != "":
        data["status"] = request.args.get('status', '')

    if 'active' in request.args and request.args['active'] != "":
        data["active"] = request.args.get('active', '')

    if 'user_email' in request.args and request.args['user_email'] != "":
        data["user_email"] = request.args.get('user_email', '')

    if 'order_by' in request.args and request.args['order_by'] != "":
        data["order_by"] = request.args.get('order_by', '')

    if 'page' in request.args and request.args['page'] != "" and request.args['page'] != "0":
        data["page"] = request.args.get('page', '')

    query = requests.get(current_app.config['API_URL'] + "/sensors", headers=headers, json=data)

    if query.status_code == 200:

        sensors = json.loads(query.text)['sensors']

        pagination = {"total_items": json.loads(query.text)["total_items"],
                      "total_pages": json.loads(query.text)["total_pages"],
                      "page": json.loads(query.text)["page"]}

        return render_template('sensores.html',
                               sensors=sensors,
                               form=form,
                               pagination=pagination,
                               request=request)

    else:
        flash("Debe iniciar sesion para continuar.", "warning")
        return redirect(url_for("login.index"))


@sensors.route('/sensor/<int:id>', methods=["POST", "GET"])
@login_required
@admin_required
def view(id):
    auth = request.cookies['access_token']
    headers = {
        'content-type': "application/json",
        'authorization': "Bearer " + auth
    }
    r = requests.get(current_app.config['API_URL'] + "/sensor/" + str(id), headers=headers)
    sensor = json.loads(r.text)
    return render_template('ver-sensor.html', sensor=sensor, link="http://127.0.0.1:5000" + "/")


@sensors.route('/sensor/delete/<int:id>', methods=["POST", "GET"])
@login_required
@admin_required
def delete(id):
    auth = request.cookies['access_token']
    headers = {
        'content-type': "application/json",
        'authorization': "Bearer " + auth
    }
    r = requests.delete(current_app.config['API_URL'] + "/sensor/" + str(id), headers=headers)
    if r.status_code == 204:
        return redirect(url_for("sensors.index"))
    else:
        flash("Debe iniciar sesion para continuar.", "warning")
        return redirect(url_for("login.index"))


@sensors.route('/agregar-sensor', methods=['POST', 'GET'])
@login_required
@admin_required
def add_sensor():
    form = CreateSensor()
    if form.validate_on_submit():
        auth = request.cookies['access_token']
        headers = {
            'content-type': "application/json",
            'authorization': "Bearer " + auth
        }
        data = {
            "name": form.name.data,
            "ip": form.ip.data,
            "port": form.port.data,
            "status": form.status.data,
            "active": form.active.data,
            "userId": form.user_id.data
        }
        r = requests.post(current_app.config['API_URL'] + "/sensors", headers=headers, json=data)
        if r.status_code == 201:
            return redirect(url_for('sensors.index'))
        else:
            return redirect(url_for('home.index'))
    return render_template('agregar-sensor.html', form=form)


@sensors.route('/modificar-sensor/<int:id>', methods=["POST", "GET"])
@login_required
@admin_required
def modify_sensor(id):
    form = CreateSensor()

    if form.validate_on_submit():
        auth = request.cookies['access_token']
        headers = {
            'content-type': "application/json",
            'authorization': "Bearer " + auth
        }
        data = {
            "name": form.name.data,
            "ip": form.ip.data,
            "port": form.port.data,
            "status": form.status.data,
            "active": form.active.data,
            "userId": form.user_id.data
        }
        r = requests.put(current_app.config['API_URL'] + "/sensor/" + str(id), headers=headers, json=data)
        if r.status_code == 201:
            return redirect(url_for('sensors.index'))
        else:
            print("Error")
    else:
        auth = request.cookies['access_token']
        headers = {
            'content-type': "application/json",
            'authorization': "Bearer " + auth
        }
        r = requests.get(current_app.config['API_URL'] + "/sensor/" + str(id), headers=headers)
        sensor = json.loads(r.text)
        form.name.data = sensor["name"]
        form.ip.data = sensor["ip"]
        form.port.data = sensor["port"]
        form.status.data = sensor["status"]
        form.active.data = sensor["active"]
        form.user_id.data = sensor["userId"]["userId"]

    return render_template('modificar-sensor.html', form=form, id=id)
