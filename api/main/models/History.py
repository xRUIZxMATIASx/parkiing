from .. import db
from main.models.User import User


class History(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    parkingId = db.Column(db.Integer, nullable=False)
    userId = db.Column(db.Integer, nullable=False)
    i_timestamp = db.Column(db.TIMESTAMP, nullable=False)
    f_timestamp = db.Column(db.TIMESTAMP, nullable=False)
    price = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<History: %r>' % (self.id)

    def to_json(self):
        history_json = {
            'id': self.id,
            'parkingId': int(self.parkingId),
            'userId': int(self.location),
            'i_timestamp': self.i_timestamp,
            'f_timestamp': self.f_timestamp,
            'price': int(self.price)
        }
        return history_json

    @staticmethod
    def from_json(history_json):
        id = history_json.get('id')
        parkingId = history_json.get('parkingId')
        userId = history_json.get('userId')
        i_timestamp = history_json.get('i_timestamp')
        f_timestamp = history_json.get('f_timestamp')
        price = history_json.get('price')

        return History(id=id,
                       parkingId=parkingId,
                       userId=userId,
                       i_timestamp=i_timestamp,
                       f_timestamp=f_timestamp,
                       price=price)

