from flask import request, Blueprint
from .. import db
from main.models import ParkingModel
from main.models import SlotsModel
from main.models import HistoryModel
from sqlalchemy import select
from datetime import datetime

parking = Blueprint('parking', __name__, url_prefix='/parking')


@parking.route('/add', methods=['POST'])
def add():
    new_json = request.get_json()
    parking = ParkingModel.from_json(new_json)
    try:
        db.session.add(parking)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return str(e), 409
    return parking.to_json(), 201

slots = Blueprint('slots', __name__, url_prefix='/slots')

# Insertar la cantidad de slots disponibles
@slots.route('/add-slots', methods=['POST'])
def add_slots():
    slots_list = list()
    new_json = request.get_json()
    amount = new_json['amount']
    del new_json['amount']
    for i in range(int(amount)):
        slots_list.append(SlotsModel.from_json(new_json))
    try:
        db.session.bulk_save_objects(slots_list)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return str(e), 409
    return "Ok", 201

# Agregar un usuario a un slots
@slots.route('/add-user', methods=['POST'])
def add_user():
    verification = db.session.query(SlotsModel).filter(SlotsModel.userId == int(request.get_json()['userId'])).first() # Verifico si el usuario ya esta en un slots
    if verification == None:
        slots = db.session.query(SlotsModel).filter(SlotsModel.parkingId == int(request.get_json()['parkingId'])).first() # Verifico que el estacionamiento tenga slot disponible
        if slots != None:
            try:
                dt = datetime.now()
                ts = datetime.timestamp(dt)
                new_json = request.get_json()
                new_json['timestamp'] = int(ts)
                new_json['state'] = 1
                for key, value in new_json.items():
                    setattr(slots, key, value)
                db.session.add(slots)
                db.session.commit()
                return slots.to_json(), 201
            except Exception as e:
                db.session.rollback()
                return str(e), 409
        else:
            return "No", 403 # El slots no tiene mas espacios disponibles
    else:
        return "No", 403 # El usuario ya esta en otro slots


# Quitar un usuario a un slots
@slots.route('/delete-user', methods=['POST'])
def delete_user():
    query = db.session.query(SlotsModel).filter(SlotsModel.userId == int(request.get_json()['userId']))
    slots = query.filter(SlotsModel.parkingId == int(request.get_json()['parkingId'])).first()
    if slots != None:
        try:
            i_timestamp = slots.timestamp
            new_json = request.get_json()
            new_json['timestamp'] = None
            new_json['userId'] = None
            new_json['state'] = 0
            for key, value in new_json.items():
                setattr(slots, key, value)
            db.session.add(slots)
            db.session.commit()
            new_json = slots.to_json()
            dt = datetime.now()
            ts = datetime.timestamp(dt)
            new_json['f_timestamp'] = int(ts)
            new_json['i_timestamp'] = int(i_timestamp)
            return new_json, 201
        except Exception as e:
            db.session.rollback()
            return str(e), 409
    else:
        return "No", 403  # El usuario no se encuentra en el slots

# Obtener un usuario de un slots
@slots.route('/get-user/<id>', methods=['GET'])
def get_user(id):
    slots = db.session.query(SlotsModel).filter(SlotsModel.userId == int(id)).first()
    if slots != None:
        try:
            return slots.to_json(), 201
        except Exception as e:
            return str(e), 409
    else:
        return "No", 403  # El usuario no se encuentra

history = Blueprint('history', __name__, url_prefix='/history')

# Guardar history
@history.route('/save-history', methods=['POST'])
def save_history():
    new_json = request.get_json()
    history = HistoryModel.from_json(new_json)
    try:
        db.session.add(history)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return str(e), 409
    return history.to_json(), 201

# Obtener ultimo registro del cliente especifico
@history.route('/get-last-history/<id>', methods=['GET'])
def get_user(id):
    new_json = request.get_json()
    history = db.session.query(HistoryModel).filter(HistoryModel.parkingId == int(id))
    history = history.filter(HistoryModel.userId == new_json['userId']).order_by(HistoryModel.id.desc()).first()
    if history != None:
        try:
            return history.to_json(), 201
        except Exception as e:
            return str(e), 409
    else:
        return "No", 403  # El history no se encuentra

# Obtener history por parking
@history.route('/get-all-history/<id>', methods=['GET'])
def get_all_user(id):
    histories = db.session.query(HistoryModel).filter(HistoryModel.parkingId == int(id)).all()
    if histories != None:
        try:
            return {'history': [history.to_json() for history in histories]}, 201
        except Exception as e:
            return str(e), 409
    else:
        return "No", 403  # El history no se encuentra
