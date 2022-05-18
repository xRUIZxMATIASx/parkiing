from .. import db
from main.models.User import User


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
        sensor_json = {
            'parkingId': self.parkingId,
            'name': str(self.name),
            'location': str(self.location),
            'space': int(self.space),
            'qr': bool(self.qr),
            'rate': bool(self.rate),
            'price': str(self.price),
            'config': str(self.config),
            'userId': self.user.to_json()
        }
        return sensor_json

    @staticmethod
    def from_json(sensor_json):
        parkingId = sensor_json.get('parkingId')
        name = sensor_json.get('name')
        location = sensor_json.get('location')
        space = sensor_json.get('space')
        qr = sensor_json.get('qr')
        rate = sensor_json.get('rate')
        price = sensor_json.get('price')
        config = sensor_json.get('config')
        userId = sensor_json.get('userId')

        return Parking(parkingId=parkingId,
                       name=name,
                       location=location,
                       space=space,
                       qr=qr,
                       rate=rate,
                       price=price,
                       config=config,
                       userId=userId)

