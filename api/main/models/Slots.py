from .. import db
from main.models.User import User


class Slots(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    parkingId = db.Column(db.Integer, nullable=False)
    userId = db.Column(db.Integer, nullable=True)
    timestamp = db.Column(db.TIMESTAMP, nullable=True)
    state = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<Slots: %r>' % (self.id)

    def to_json(self):
        slots_json = {
            'id': self.id,
            'parkingId': int(self.parkingId),
            'userId': self.userId,
            'timestamp': self.timestamp,
            'state': self.state
        }
        return slots_json

    @staticmethod
    def from_json(slots_json):
        id = slots_json.get('id')
        parkingId = slots_json.get('parkingId')
        userId = slots_json.get('userId')
        timestamp = slots_json.get('timestamp')
        state = slots_json.get('state')

        return Slots(id=id,
                       parkingId=parkingId,
                       userId=userId,
                       timestamp=timestamp,
                       state=state)

