from base64 import b64decode

from flask import request
from flask_login import UserMixin
import jwt
from jwt import decode, exceptions
import os
from main import login_manager

class LoggedUser(UserMixin):
    def __init__(self, id, admin, parkingId):
        self.id = id
        self.admin = admin
        self.parkingId = parkingId

@login_manager.request_loader
def load_user(request):
    if 'access_token' in request.cookies:
        try:
            decoded_token = decode(request.cookies['access_token'], options={"verify_signature": False}, algorithms="HS256")
            user_data = decoded_token['sub']
            user = LoggedUser(
                id=user_data['userId'],
                admin=user_data['admin'],
                parkingId=user_data['parkingId']
            )
            return user
        except exceptions.DecodeError as e:
            print(e)
        except exceptions.InvalidTokenError as e:
            print(e)
        except Exception as e:
            print(e)
    return None
