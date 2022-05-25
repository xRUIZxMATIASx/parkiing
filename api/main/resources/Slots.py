from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import SlotsModel
#from flask_jwt_extended import jwt_required, get_jwt_identity, jwt_optional


class Slots(Resource):

    #@jwt_required
    def get(self, id):
        slots = db.session.query(SlotsModel).get_or_404(id)
        return slots.to_json()

    #@jwt_required
    def put(self, id):
        slots = db.session.query(SlotsModel).get_or_404(id)
        for key, value in request.get_json().items():
            setattr(slots, key, value)
        db.session.add(slots)
        db.session.commit()
        return slots.to_json(), 201

    #@jwt_required
    def delete(self, id):
        slots = db.session.query(SlotsModel).get_or_404(id)
        db.session.delete(slots)
        db.session.commit()
        return "DELETE COMPLETE", 204
