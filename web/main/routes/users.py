import json
import requests
from flask import Blueprint, render_template, url_for, flash, request, current_app
from flask_login import login_required
from main import admin_required
from main.forms.Users import CreateUser
from main.forms.Users import EditUser
from werkzeug.utils import redirect

users = Blueprint('users', __name__, url_prefix='/')


@users.route('/usuarios', methods=['POST', 'GET'])
@login_required
@admin_required
def index():
    auth = request.cookies['access_token']
    headers = {
        'content-type': "application/json",
        'authorization': "Bearer " + auth
    }
    r = requests.get(current_app.config['API_URL'] + "/users", headers=headers)

    if r.status_code == 200:
        users = json.loads(r.text)["users"]
        return render_template('usuarios.html', users=users)
    else:
        flash("Debe iniciar sesion para continuar.", "warning")
        return redirect(url_for("login.index"))


@users.route('/user/<int:id>', methods=["POST", "GET"])
@login_required
@admin_required
def view(id):
    auth = request.cookies['access_token']
    headers = {
        'content-type': "application/json",
        'authorization': "Bearer " + auth
    }
    r = requests.get(current_app.config['API_URL'] + "/user/" + str(id), headers=headers)
    if r.status_code == 200:
        user = json.loads(r.text)
        return render_template('ver-usuario.html', id=id, user=user, link="http://127.0.0.1:5000" + "/")
    else:
        flash("Debe iniciar sesion para continuar.", "warning")
        return redirect(url_for("login.index"))


@users.route('/user/delete/<int:id>', methods=["POST", "GET"])
@login_required
@admin_required
def delete(id):
    auth = request.cookies['access_token']
    headers = {
        'content-type': "application/json",
        'authorization': "Bearer " + auth
    }
    r = requests.delete(current_app.config['API_URL'] + "/user/" + str(id), headers=headers)
    if r.status_code == 204:
        return redirect(url_for("users.index"))
    else:
        flash("Debe iniciar sesion para continuar.", "warning")
        return redirect(url_for("login.index"))


@users.route('/agregar-usuario', methods=['POST', 'GET'])
@login_required
@admin_required
def add_user():
    form = CreateUser()
    if form.validate_on_submit():
        data = {
            "email": form.email.data,
            "password": form.password.data,
            "admin": form.admin.data
        }
        r = requests.post(current_app.config['API_URL'] + "/auth/register",
                          headers={'content-type': 'application/json'}, json=data)
        if r.status_code == 201:
            return redirect(url_for('users.index'))
        else:
            print("Error")
    return render_template('agregar-usuario.html', form=form)


@users.route('/modificar-usuario/<int:id>', methods=["POST", "GET"])
@login_required
@admin_required
def modify_user(id):
    form = EditUser()
    if form.validate_on_submit():
        auth = request.cookies['access_token']
        headers = {
            'content-type': "application/json",
            'authorization': "Bearer " + auth
        }
        data = {
            "email": form.email.data,
            "admin": form.admin.data
        }

        r = requests.put(current_app.config['API_URL'] + "/user/" + str(id), headers=headers, data=json.dumps(data))
        if r.status_code == 201:
            return redirect(url_for("users.index"))
        else:
            flash("Error en la consulta", "error")
            return redirect(url_for("home.index"))
    else:
        auth = request.cookies['access_token']
        headers = {
            'content-type': "application/json",
            'authorization': "Bearer " + auth
        }
        r = requests.get(current_app.config['API_URL'] + "/user/" + str(id), headers=headers)
        user = json.loads(r.text)
        form.email.data = user["email"]
        form.admin.data = user["admin"]

    return render_template('modificar-usuario.html', form=form, id=id)
