from flask import request, Blueprint
from .. import db
from main.models import UserModel
from flask_jwt_extended import jwt_required
from flask_jwt_extended import create_access_token
from main.mail.functions import sendMail

auth = Blueprint('auth', __name__, url_prefix='/auth')

@auth.route('/login', methods=['POST'])
def login():
    json_request = request.get_json()
    user = db.session.query(UserModel).filter(UserModel.email == json_request.get("email")).first_or_404()
    if user.validate_pass(request.get_json().get('password')):
        access_token = create_access_token(identity=user.to_json())
        data = '{"id":"'+str(user.userId)+'","email":"'+str(user.email)+'", "access_token":"'+access_token+'", "admin":"'+str(user.admin)+'"}'
        return data, 200
    else:
        return "Incorrect password", 204


@auth.route('/register', methods=['POST'])
def register():
    user = UserModel.from_json(request.get_json())
    exists = db.session.query(UserModel).filter(UserModel.email == user.email).scalar() is not None
    if exists:
        return "Duplicated mail", 409
    else:
        try:
            db.session.add(user)
            #sent = sendMail(user.email, "Register", "mail/register", user=user)
            if True:#sent:
                db.session.commit()
            else:
                db.session.rollback()
                return str(sent), 502
        except Exception as e:
            db.session.rollback()
            return str(e), 409
        return user.to_json(), 201

@auth.route('/recover-password', methods=['POST'])
def recover_password():
    user = db.session.query(UserModel).filter(UserModel.email == request.get_json().get("email")).first()
    if user != None:
        try:
            sendMail(user.email, "Recover Password", "mail/recover", user=user)
            return "Enviado", 200
        except Exception as e:
            return str(e), 500
    else:
        return "User not found", 409


@auth.route('/recover-password/<password>', methods=['POST'])
def change_password_forgotten(password):
    user = db.session.query(UserModel).filter(UserModel.email == request.get_json().get("email")).first()
    if user != None:
        if user.password == password:
            user.password = UserModel.generate_pass(str(request.get_json().get('password')))
            db.session.add(user)
            db.session.commit()
            return "Password changed", 201
        else:
            return "Incorrect link", 204
    else:
        return "User not found", 409



@auth.route('/change-password', methods=['POST'])
@jwt_required
def change_password():
    user = db.session.query(UserModel).filter(UserModel.email == request.get_json().get("email")).first()
    if user != None:
        if user.validate_pass(request.get_json().get('old_password')):
            user.password = UserModel.generate_pass(str(request.get_json().get('password')))
            db.session.add(user)
            db.session.commit()
            return "Password changed", 201
        else:
            return "Incorrect password", 204
    else:
        return "User not found", 409

