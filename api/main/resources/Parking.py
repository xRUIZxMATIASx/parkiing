import math

from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import ParkingModel, UserModel
#from flask_jwt_extended import jwt_required, jwt_optional

class Parking(Resource):

    #@jwt_required
    def get(self, id):
        parking = db.session.query(ParkingModel).get_or_404(id)
        return parking.to_json()


    #@jwt_required
    def delete(self, id):
        parking = db.session.query(ParkingModel).get_or_404(id)
        db.session.delete(parking)
        db.session.commit()
        return "DELETE COMPLETE", 204

    #@jwt_required
    def put(self, id):
        parking = db.session.query(ParkingModel).get_or_404(id)
        for key, value in request.get_json().items():
            setattr(parking, key, value)
        db.session.add(parking)
        db.session.commit()
        return request.get_json(), 201


class Parkings(Resource):

    def get(self, params):

        coordinates = params.split('&')[0]
        max_distance = float(params.split('&')[1])
        parkings = db.session.query(ParkingModel).all()

        new_parkings = list()

        for parking in parkings:
            try:
                distance = float(self.calculate_distance(float(coordinates.split(",")[0]), float(coordinates.split(",")[1]), float(parking.location.split(",")[0]), float(parking.location.split(",")[1]))) * 1000
                if distance < max_distance:
                    new_parkings.append(parking)
            except Exception as e:
                pass

        return jsonify({'parkings': [parking.to_json() for parking in new_parkings]})

    def calculate_distance(self, lat1, long1, lat2, long2):
        degrees_to_radians = math.pi/180.0
        phi1 = (90.0 - lat1)*degrees_to_radians
        phi2 = (90.0 - lat2)*degrees_to_radians
        theta1 = long1*degrees_to_radians
        theta2 = long2*degrees_to_radians
        cos = (math.sin(phi1)*math.sin(phi2)*math.cos(theta1 - theta2) + math.cos(phi1)*math.cos(phi2))
        arc = math.acos(cos)*6371
        return arc
