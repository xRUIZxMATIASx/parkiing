from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import ParkingModel, UserModel
#from flask_jwt_extended import jwt_required, jwt_optional

class Parking(Resource):

    #@jwt_required
    def get(self, id):
        parking = db.session.query(Parking).get_or_404(id)
        return parking.to_json()

    #@jwt_required
    def delete(self, id):
        parking = db.session.query(Parking).get_or_404(id)
        db.session.delete(parking)
        db.session.commit()
        return "DELETE COMPLETE", 204

    #@jwt_required
    def put(self, id):
        parking = db.session.query(Parking).get_or_404(id)
        for key, value in request.get_json().items():
            setattr(parking, key, value)
        db.session.add(parking)
        db.session.commit()
        return request.get_json(), 201


class Parkings(Resource):
    def get(self):
        page = 1
        per_page = 10
        filter = request.get_json().items()
        parkings = db.session.query(parkingModel)
        for key, value in filter:
            if key == "parkingId":
                parkings = parkings.filter(parkingModel.parkingId == value)
            if key == "name":
                parkings = parkings.filter(parkingModel.name.like("%" + value + "%"))
            if key == "status":
                parkings = parkings.filter(parkingModel.status == value)
            if key == "active":
                parkings = parkings.filter(parkingModel.active == value)
            if key == "user_email":
                parkings = parkings.join(parkingModel.user).filter(UserModel.email.like("%" + value + "%"))
            if key == "order_by":
                if value == "name[desc]":
                    parkings = parkings.order_by(parkingModel.name.desc())
                if value == "name[asc]":
                    parkings = parkings.order_by(parkingModel.name.asc())
                if value == "active[desc]":
                    parkings = parkings.order_by(parkingModel.active.desc())
                if value == "active[asc]":
                    parkings = parkings.order_by(parkingModel.active.asc())
                if value == "status[desc]":
                    parkings = parkings.order_by(parkingModel.status.desc())
                if value == "status[asc]":
                    parkings = parkings.order_by(parkingModel.status.asc())

            if key == "page":
                page = value

            if key == "per_page":
                per_page = int(value)

        parkings = parkings.paginate(page, per_page, True, 10)
        return jsonify({'parkings': [parking.to_json() for parking in parkings.items],
                            "total_items": parkings.total,
                            "total_pages": parkings.pages,
                            "page": page})

