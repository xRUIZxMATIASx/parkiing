from flask import Blueprint, render_template
import flask_login
from flask_login import login_required
from flask import Blueprint, render_template, request, url_for, current_app
from main.resources.auth import LoggedUser

home = Blueprint('index', __name__, url_prefix='/')


@home.route('/')
@home.route('/index')
@login_required
def index():
    return render_template('home.html', current_user=flask_login.current_user)
