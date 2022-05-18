import os
from flask import Flask
from dotenv import load_dotenv
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

from main.config import DevelopmentConfig

from flask_mail import Mail

api = Api()
db = SQLAlchemy()
jwt = JWTManager()
mailSender = Mail()

def create_app():
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig())
    db.init_app(app)

    app.config["JWT_SECRET_KEY"] = "qwertyuiop"
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES'))
    jwt.init_app(app)


    import main.resources as resources
    from main.auth import routes
    from main.routes import routes as routes2

    api.add_resource(resources.ParkingResource, '/parking/<id>')
    api.add_resource(resources.ParkingsResource, '/parkings/<params>')
    api.add_resource(resources.UserResource, '/user/<id>')
    api.add_resource(resources.GenerateQRResource, '/generateqr/<id>')
    api.init_app(app)

    app.register_blueprint(routes.auth)
    app.register_blueprint(routes2.parking)

    app.config['MAIL_HOSTNAME'] = os.getenv('MAIL_HOSTNAME')
    app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
    app.config['MAIL_PORT'] = os.getenv('MAIL_PORT')
    app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS')
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
    app.config['FLASKY_MAIL_SENDER'] = os.getenv('FLASKY_MAIL_SENDER')
    mailSender.init_app(app)

    return app
