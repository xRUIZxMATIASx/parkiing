from flask import request, Blueprint
from .. import db
from main.models import ParkingModel
from main.models import SlotsModel
from sqlalchemy import select

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

slots = Blueprint('slots', __name__, url_prefix='/slots')

# Insertar la cantidad de slots disponibles
@slots.route('/add-slots/<amount>', methods=['POST'])
def add_slots(amount):
    slots_list = list()
    for i in range(int(amount)):
        slots_list.append(SlotsModel.from_json(request.get_json()))
    try:
        db.session.bulk_save_objects(slots_list)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return str(e), 409
    return "Ok", 201

# Agregar un usuario a un slot
@slots.route('/add-user/<id>', methods=['POST'])
def add_user(id):

    slots = db.session.query(SlotsModel).filter(SlotsModel.parkingId == int(id)).first()
    if slots != None:
        for key, value in request.get_json().items():
            setattr(slots, key, value)
        db.session.add(slots)
        db.session.commit()
        return slots.to_json(), 201
    else:
        return "No", 403


# Quitar un usuario a un slot
@slots.route('/delete-user', methods=['POST'])
def delete_user():
    db.session.execute(select().where(SlotsModel.userId == Address.user_id)).all()
    slots = db.session.query(SlotsModel).get_or_404(id)
    for key, value in request.get_json().items():
        setattr(slots, key, value)
    db.session.add(slots)
    db.session.commit()
    return slots.to_json(), 201
