from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import ParkingModel, UserModel
#from flask_jwt_extended import jwt_required, jwt_optional


class Parking(Resource):

    #@jwt_required
    def get(self, id):
        sensor = db.session.query(Parking).get_or_404(id)
        return sensor.to_json()

    #@jwt_required
    def delete(self, id):
        sensor = db.session.query(Parking).get_or_404(id)
        db.session.delete(sensor)
        db.session.commit()
        return "DELETE COMPLETE", 204

    #@jwt_required
    def put(self, id):
        sensor = db.session.query(Parking).get_or_404(id)
        for key, value in request.get_json().items():
            setattr(sensor, key, value)
        db.session.add(sensor)
        db.session.commit()
        return request.get_json(), 201


"""
class Sensors(Resource):
    @jwt_optional
    def get(self):
        page = 1
        per_page = 10
        filter = request.get_json().items()
        sensors = db.session.query(SensorModel)
        for key, value in filter:
            if key == "sensorId":
                sensors = sensors.filter(SensorModel.sensorId == value)
            if key == "name":
                sensors = sensors.filter(SensorModel.name.like("%" + value + "%"))
            if key == "status":
                sensors = sensors.filter(SensorModel.status == value)
            if key == "active":
                sensors = sensors.filter(SensorModel.active == value)
            if key == "user_email":
                sensors = sensors.join(SensorModel.user).filter(UserModel.email.like("%" + value + "%"))
            if key == "order_by":
                if value == "name[desc]":
                    sensors = sensors.order_by(SensorModel.name.desc())
                if value == "name[asc]":
                    sensors = sensors.order_by(SensorModel.name.asc())
                if value == "active[desc]":
                    sensors = sensors.order_by(SensorModel.active.desc())
                if value == "active[asc]":
                    sensors = sensors.order_by(SensorModel.active.asc())
                if value == "status[desc]":
                    sensors = sensors.order_by(SensorModel.status.desc())
                if value == "status[asc]":
                    sensors = sensors.order_by(SensorModel.status.asc())

            if key == "page":
                page = value

            if key == "per_page":
                per_page = int(value)

        sensors = sensors.paginate(page, per_page, True, 10)
        return jsonify({'sensors': [sensor.to_json() for sensor in sensors.items],
                            "total_items": sensors.total,
                            "total_pages": sensors.pages,
                            "page": page})

    @jwt_required
    def post(self):
        sensor = SensorModel.from_json(request.get_json())
        db.session.add(sensor)
        db.session.commit()
        return request.get_json(), 201
"""