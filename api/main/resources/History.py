from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import HistoryModel
#from flask_jwt_extended import jwt_required, get_jwt_identity, jwt_optional


class History(Resource):

    #@jwt_required
    def get(self, id):
        history = db.session.query(HistoryModel).get_or_404(id)
        return history.to_json()

    #@jwt_required
    def put(self, id):
        history = db.session.query(HistoryModel).get_or_404(id)
        for key, value in request.get_json().items():
            setattr(history, key, value)
        db.session.add(history)
        db.session.commit()
        return history.to_json(), 201

    #@jwt_required
    def delete(self, id):
        history = db.session.query(HistoryModel).get_or_404(id)
        db.session.delete(history)
        db.session.commit()
        return "DELETE COMPLETE", 204
