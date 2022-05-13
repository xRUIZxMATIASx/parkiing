import datetime
import json
import requests
from flask import Blueprint, render_template, redirect, url_for, current_app, request
from flask import flash
from flask_login import login_required
from main.forms.Seisms import Seism
modify_seism = Blueprint('modify_seism', __name__, url_prefix='/')
from main.forms.Seisms import UnverifiedSeismsSearch


seisms_no_verified = Blueprint('seisms_no_verified', __name__, url_prefix='/')


@seisms_no_verified.route('/sismos-no-verificados', methods=["POST", "GET"])
@login_required
def index():
    auth = request.cookies['access_token']
    headers = {
        'content-type': "application/json",
        'authorization': "Bearer " + auth
    }

    form = UnverifiedSeismsSearch(request.args, meta={'csrf': False})

    query = requests.get(current_app.config['API_URL'] + "/sensors", headers=headers, json={})
    sensors = json.loads(query.text)["sensors"]

    form.seismId.choices = [(int(sensor['sensorId']), sensor['name']) for sensor in sensors]
    form.seismId.choices.insert(0, [-1, "Seleccione"])

    data = {}

    if 'seismId' in request.args and request.args.get('seismId', '') != '-1' and request.args.get('seismId', '') != '':
        data["sensorId"] = request.args.get('seismId', '')

    if "from_date" in request.args and request.args["from_date"] != "":
        date = datetime.datetime.strptime(request.args.get("from_date", ""), "%Y-%m-%d %H:%M:%S")
        data["from_date"] = datetime.datetime.strftime(date, "%Y-%m-%d %H:%M:%S")

    if "to_date" in request.args and request.args["to_date"] != "":
        date = datetime.datetime.strptime(request.args.get("to_date", ""), "%Y-%m-%d %H:%M:%S")
        data["to_date"] = datetime.datetime.strftime(date, "%Y-%m-%d %H:%M:%S")

    if 'order_by' in request.args and request.args['order_by'] != "":
        data["order_by"] = request.args.get('order_by', '')

    if 'page' in request.args and request.args['page'] != "" and request.args['page'] != "0":
        data["page"] = request.args.get('page', '')

    query = requests.get(current_app.config['API_URL'] + "/unverified-seisms", headers=headers, json=data)

    if query.status_code == 200:

        seisms_no_verified = json.loads(query.text)['unverified-seisms']

        pagination = {"total_items": json.loads(query.text)["total_items"],
                      "total_pages": json.loads(query.text)["total_pages"],
                      "page": json.loads(query.text)["page"]}

        return render_template('sismos-no-verificados.html',
                               seisms_no_verified=seisms_no_verified,
                               form=form,
                               pagination=pagination,
                               request=request)

    else:
        flash("Debe iniciar sesion para continuar.", "warning")
        return redirect(url_for("login.index"))


@seisms_no_verified.route('/sismos-no-verificados/<int:id>', methods=["POST", "GET"])
@login_required
def view(id):
    auth = request.cookies['access_token']
    headers = {
        'content-type': "application/json",
        'authorization': "Bearer " + auth
    }
    r = requests.get(current_app.config['API_URL'] + "/unverified-seism/" + str(id), headers=headers)
    if r.status_code == 200:
        seism_no_verified = json.loads(r.text)
        return render_template('ver-sismo-no-verificado.html', seism_no_verified=seism_no_verified,
                               url="http://127.0.0.1:5000")
    else:
        flash("Debe iniciar sesion para continuar.", "warning")
        return redirect(url_for("login.index"))


@seisms_no_verified.route('/modificar-sismo/<int:id>', methods=['POST', 'GET'])
@login_required
def modify_seism(id):
    form = Seism()
    if form.validate_on_submit():
        auth = request.cookies['access_token']
        headers = {
            'content-type': "application/json",
            'authorization': "Bearer " + auth
        }
        data = {
            "depth": form.depth.data,
            "magnitude": form.magnitude.data,
            "verified": form.verified.data
        }

        r = requests.put(current_app.config['API_URL'] + "/unverified-seism/" + str(id), headers=headers, json=data)
        if r.status_code == 201:
            return redirect(url_for('seisms_no_verified.index'))
        else:
            print("Error")
    else:
        auth = request.cookies['access_token']
        headers = {
            'content-type': "application/json",
            'authorization': "Bearer " + auth
        }
        r = requests.get(current_app.config['API_URL'] + "/unverified-seism/" + str(id), headers=headers)
        seism_no_verified = json.loads(r.text)
        form.depth.data = seism_no_verified["depth"]
        form.magnitude.data = seism_no_verified["magnitude"]
        form.verified.data = seism_no_verified["verified"]

    return render_template('modificar-sismo.html', form=form, url=current_app.config['API_URL'], id=id)
