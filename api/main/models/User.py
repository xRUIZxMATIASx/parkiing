from .. import db
from werkzeug.security import generate_password_hash, check_password_hash
#from main.models.Parking import Parking

class User(db.Model):

    userId = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), nullable=False, unique=True, index=True)
    password = db.Column(db.String(100), nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)
    parkingId = db.Column(db.Integer, nullable=True)
    parking = db.relationship("Parking", back_populates="user")

    @property
    def plain_password(self):
        raise AttributeError("Password cant be read")
    @plain_password.setter
    def plain_password(self, password):
        self.password = generate_password_hash(password)

    def validate_pass(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '<User: %r %r >' % (self.email, self.admin)

    def to_json(self):
        #self.parking = db.session.query(Parking).get_or_404(self.parkingId)
        user_json = {
            'userId': self.userId,
            'email': str(self.email),
            'admin': self.admin,
            'parkingId': self.parkingId #self.parking.to_json()
        }
        return user_json

    def to_json_public(self):
        user_json = {
            'userId': self.userId,
            'email': str(self.email),
            'admin': self.admin,
            'parkingId': self.parkingId
        }
        return user_json

    @staticmethod
    def from_json(user_json):
        email = user_json.get('email')
        password = user_json.get('password')
        admin = user_json.get('admin')
        parkingId = user_json.get('parkingId')

        return User(email=email,
                    plain_password=password,
                    admin=admin,
                    parkingId=parkingId)

    @staticmethod
    def generate_pass(password):
        return generate_password_hash(password)
