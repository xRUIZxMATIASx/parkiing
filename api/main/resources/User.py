from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import UserModel
#from flask_jwt_extended import jwt_required, get_jwt_identity, jwt_optional


class User(Resource):

    #@jwt_required
    def get(self, id):
        user = db.session.query(UserModel).get_or_404(id)
        return user.to_json()

    #@jwt_required
    def put(self, id):
        user = db.session.query(UserModel).get_or_404(id)
        for key, value in request.get_json().items():
            setattr(user, key, value)
        db.session.add(user)
        db.session.commit()
        return user.to_json(), 201

    #@jwt_required
    def delete(self, id):
        user = db.session.query(UserModel).get_or_404(id)
        db.session.delete(user)
        db.session.commit()
        return "DELETE COMPLETE", 204



"""
class Users(Resource):

    #@jwt_optional
    def get(self):
        users = db.session.query(UserModel).all()
        current_user = get_jwt_identity()
        if current_user:
            return jsonify({'users': [user.to_json() for user in users]})
        else:
            return jsonify({'users': [user.to_json_public() for user in users]})

"""