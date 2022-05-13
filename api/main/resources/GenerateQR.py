from flask_restful import Resource
from flask import request, jsonify
from .. import db
import qrcode
#from flask_jwt_extended import jwt_required, jwt_optional


"""
El codigo

Click en generar codigo QR -> obtener el id de usuario y pasar por parametro -> devolver QR

"""

class GenerateQR(Resource):

    #@jwt_required
    def get(self, id):
        img = qrcode.make("hhttp://localhost:8080/?id="+id)
        #f = open("output.png", "wb")
        #img.save(f)
        #f.close()

        return True
