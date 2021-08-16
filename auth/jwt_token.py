import jwt
import datetime
import models

import config


def generate_token(user_name, private_key):
    now_time = datetime.datetime.now()
    user = config.SESSION.query(models.Employee).filter_by(Full_name=user_name).first()
    payload = {
        'Sub': user_name,
        'User_id': user.id if user else None,
        'Position_id': user.Position_id if user else None,
        'iat': now_time

    }
    token = jwt.encode(payload, private_key, algorithm="HS256")
    # jwt.decode(token, private_key, algorithms=['HS256'])
    return token


def decode_token(token, secret_key):
    return jwt.decode(token, secret_key, algorithms=['HS256'])
