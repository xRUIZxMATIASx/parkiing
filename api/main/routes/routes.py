from flask import request, Blueprint
from .. import db
from main.models import ParkingModel

parking = Blueprint('parking', __name__, url_prefix='/parking')


@parking.route('/add', methods=['POST'])
def add():
    parking = ParkingModel.from_json(request.get_json())
    try:
        db.session.add(parking)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return str(e), 409
    return parking.to_json(), 201
