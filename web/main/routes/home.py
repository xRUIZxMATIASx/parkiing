from flask import Blueprint, render_template
import flask_login
from flask_login import login_required
from flask import Blueprint, render_template, request, url_for, current_app
from main.resources.auth import LoggedUser
from sphinx.util import requests

home = Blueprint('index', __name__, url_prefix='/')


@home.route('/')
@home.route('/index')
@login_required
def index():
    if flask_login.current_user.admin:
        return render_template('home.html', current_user=flask_login.current_user)
    else:
        # Aca debo traer todos los parking
        url = str(current_app.config['API_URL']) + str('/user/' + str(flask_login.current_user.id))
        r = requests.get(url=url)
        return render_template('home-common.html', current_user=flask_login.current_user)
