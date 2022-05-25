import os
from functools import wraps

from flask import Flask, flash, url_for
from dotenv import load_dotenv
from flask_wtf import CSRFProtect
from flask_login import LoginManager, current_user
from werkzeug.utils import redirect

login_manager = LoginManager()

@login_manager.unauthorized_handler
def unauthorized_callback():
    flash("Debe iniciar sesion para continuar.", "warning")
    return redirect(url_for("login.index"))

def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kws):
        if not current_user.admin:
            flash('No tiene autorizacion para entrar a este apartado', 'warning')
            return redirect(url_for('home.index'))
        return fn(*args, **kws)
    return wrapper


def create_app():

    app = Flask(__name__)
    load_dotenv()
    app.config['API_URL'] = os.getenv('API_URL')
    app.config['WEB_URL'] = os.getenv('WEB_URL')

    csrf = CSRFProtect(app)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

    from main.routes import login, home, users, config, parkings
    login_manager.init_app(app)
    app.register_blueprint(login)
    app.register_blueprint(home)
    app.register_blueprint(users)
    app.register_blueprint(config)
    app.register_blueprint(parkings)

    csrf.init_app(app)
    return app
