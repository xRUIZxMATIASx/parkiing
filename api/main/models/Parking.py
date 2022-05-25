from .. import db
from flask import jsonify
from main.models.User import User
from main.models.Slots import Slots


class Parking(db.Model):

    parkingId = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(30), nullable=False)
    space = db.Column(db.Integer, nullable=False)
    qr = db.Column(db.String(2000), nullable=True)
    rate = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    config = db.Column(db.String(100), nullable=False)
    userId = db.Column(db.Integer, db.ForeignKey("user.userId"))
    user = db.relationship("User", back_populates="parking", uselist=False, single_parent=True)



    def __repr__(self):
        return '<Parking: %r %r %r %r %r>' % (self.name, self.location, self.space, self.qr, self.rate)



    def to_json(self):
        self.user = db.session.query(User).get_or_404(self.userId)
        self.slots = db.session.query(Slots).filter(Slots.parkingId == int(self.parkingId)).all()
        parking_json = {
            'parkingId': self.parkingId,
            'name': str(self.name),
            'location': str(self.location),
            'space': int(self.space),
            'qr': str(self.qr),
            'rate': int(self.rate),
            'price': str(self.price),
            'config': str(self.config),
            'userId': self.user.to_json(),
            'slots': {'slots': [slot.to_json() for slot in self.slots]}
        }
        return parking_json

    @staticmethod
    def from_json(parking_json):
        parkingId = parking_json.get('parkingId')
        name = parking_json.get('name')
        location = parking_json.get('location')
        space = parking_json.get('space')
        qr = parking_json.get('qr')
        rate = parking_json.get('rate')
        price = parking_json.get('price')
        config = parking_json.get('config')
        userId = parking_json.get('userId')

        return Parking(parkingId=parkingId,
                       name=name,
                       location=location,
                       space=space,
                       qr=qr,
                       rate=rate,
                       price=price,
                       config=config,
                       userId=userId)

