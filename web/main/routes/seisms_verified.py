import csv
import datetime
import io
import json
import requests
from flask import Blueprint, render_template, request, flash, url_for, make_response, current_app
from flask_login import login_required
from werkzeug.utils import redirect
from main.forms.login import Login
from main.forms.Seisms import VerifiedSeismsSearch

seisms_verified = Blueprint('seisms_verified', __name__, url_prefix='/')


def get_verified_seisms():
    headers = {
        'content-type': "application/json"
    }

    form = VerifiedSeismsSearch(request.args, meta={'csrf': False})

    query = requests.get(current_app.config['API_URL'] + "/sensors", headers=headers, json={})
    sensors = json.loads(query.text)["sensors"]

    form.sensor_name.choices = [(int(sensor['sensorId']), sensor['name']) for sensor in sensors]
    form.sensor_name.choices.insert(0, [-1, "Seleccione"])

    data = {}

    file_name = "sismos verificados"

    if 'sensor_name' in request.args and request.args.get('sensor_name', '') != '-1' and request.args.get('sensor_name', '') != '':
        data["sensor_name"] = request.args.get('sensor_name', '')
        file_name = file_name + "-" + str(data["sensor_name"])

    if "from_date" in request.args and request.args["from_date"] != "":
        date = datetime.datetime.strptime(request.args.get("from_date", ""), "%Y-%m-%d %H:%M:%S")
        data["from_date"] = datetime.datetime.strftime(date, "%Y-%m-%d %H:%M:%S")
        file_name = file_name + "-" + str(datetime.datetime.strftime(date, "%Y%m%dT%H%M%S"))

    if "to_date" in request.args and request.args["to_date"] != "":
        date = datetime.datetime.strptime(request.args.get("to_date", ""), "%Y-%m-%d %H:%M:%S")
        data["to_date"] = datetime.datetime.strftime(date, "%Y-%m-%d %H:%M:%S")
        file_name = file_name + "-" + str(datetime.datetime.strftime(date, "%Y%m%dT%H%M%S"))

    if 'depth_min' in request.args and request.args.get('depth_min', '') != '':
        data["depth_min"] = request.args.get('depth_min', '')
        file_name = file_name + "-" + str(data["depth_min"])

    if 'depth_max' in request.args and request.args.get('depth_max', '') != '':
        data["depth_max"] = request.args.get('depth_max', '')
        file_name = file_name + "-" + str(data["depth_max"])

    if 'magnitude_min' in request.args and request.args.get('magnitude_min', '') != '':
        data["magnitude_min"] = request.args.get('magnitude_min', '')
        file_name = file_name + "-" + str(data["magnitude_min"])

    if 'magnitude_max' in request.args and request.args.get('magnitude_max', '') != '':
        data["magnitude_max"] = request.args.get('magnitude_max', '')
        file_name = file_name + "-" + str(data["magnitude_max"])

    if 'order_by' in request.args and request.args['order_by'] != "":
        data["order_by"] = request.args.get('order_by', '')
        file_name = file_name + "-" + str(data["order_by"])

    if 'page' in request.args and request.args['page'] != "" and request.args['page'] != "0":
        data["page"] = request.args.get('page', '')

    if 'download' in request.args:
        if request.args.get('download', '') == 'Descargar en CSV':
            code = 200
            page = 1
            seisms_list = []

            while code == 200:
                data['page'] = page

                query = requests.get(current_app.config['API_URL'] + "/verified-seisms", headers=headers, json=data)
                code = query.status_code

                if query.status_code == 200:
                    verified_seisms = json.loads(query.text)["verified-seisms"]

                    for seism in verified_seisms:
                        seism_dict = {
                            'datetime': seism["datetime"],
                            'depth': seism["depth"],
                            'magnitude': seism["magnitude"],
                            'latitude': seism["latitude"],
                            'longitude': seism["longitude"],
                            'sensor': seism["sensorId"]["name"]
                        }
                        seisms_list.append(seism_dict)
                    page += 1

            if seisms_list:
                si = io.StringIO()
                fc = csv.DictWriter(si, fieldnames=seisms_list[0].keys(), )

                fc.writeheader()
                fc.writerows(seisms_list)

                output = make_response(si.getvalue())

                output.headers["Content-Disposition"] = "attachment; filename=" + file_name + ".csv"
                output.headers["Content-type"] = "text/csv"

                return output

    query = requests.get(current_app.config['API_URL'] + "/verified-seisms", headers=headers, json=data)

    if query.status_code == 200:

        seisms_verified = json.loads(query.text)['verified-seisms']

        pagination = {"total_items": json.loads(query.text)["total_items"],
                      "total_pages": json.loads(query.text)["total_pages"],
                      "page": json.loads(query.text)["page"]}

        return seisms_verified, form, pagination, request

    else:
        return redirect(url_for("login.index"))


@seisms_verified.route('/sismos-verificados')
@login_required
def index():
    seisms_verified, form, pagination, request = None, None, None, None
    try:
        seisms_verified, form, pagination, request = get_verified_seisms()
    except:
        return get_verified_seisms()
    return render_template('sismos-verificados.html',
                           seisms_verified=seisms_verified,
                           form=form,
                           pagination=pagination,
                           request=request)


@seisms_verified.route('/sismos-verificados/<int:id>', methods=["POST", "GET"])
@login_required
def view(id):
    auth = request.cookies['access_token']
    headers = {
        'content-type': "application/json",
        'authorization': "Bearer " + auth
    }
    r = requests.get(current_app.config['API_URL'] + "/verified-seism/" + str(id), headers=headers)
    if r.status_code == 200:
        seism_verified = json.loads(r.text)
        return render_template('ver-sismo-verificado.html', seism_verified=seism_verified, url=current_app.config['WEB_URL'])
    else:
        flash("Debe iniciar sesion para continuar.", "warning")
        return redirect(url_for("login.index"))

@seisms_verified.route('/sismos-verificados-2/<int:id>', methods=["POST", "GET"])
def view2(id):
    headers = {
        'content-type': "application/json"
    }
    r = requests.get(current_app.config['API_URL'] + "/verified-seism/" + str(id), headers=headers)
    if r.status_code == 200:
        seism_verified = json.loads(r.text)
        form_login = Login()
        return render_template('ver-sismo-verificado-2.html', form_login=form_login, seism_verified=seism_verified, url=current_app.config['WEB_URL'])
    else:
        return redirect(url_for("login.index"))
