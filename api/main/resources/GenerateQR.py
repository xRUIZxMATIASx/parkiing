import json
import os
from flask_restful import Resource
import base64
import qrcode
import io
from main.models import ParkingModel
from .. import db

class GenerateQR(Resource):

    #@jwt_required
    def get(self, id):
        img = qrcode.make(os.getenv('API_URL') + "parking/search/"+id)
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()
        encoded_string = str(base64.b64encode(img_byte_arr).decode("utf-8"))

        parking = db.session.query(ParkingModel).get_or_404(id)
        json_parking = parking.to_json()
        json_parking["qr"] = encoded_string
        del json_parking["parkingId"]
        del json_parking["userId"]
        for key, value in json_parking.items():
            setattr(parking, key, value)
        db.session.add(parking)
        db.session.commit()

        return encoded_string, 201
