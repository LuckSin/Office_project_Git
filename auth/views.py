import config
from flask import jsonify, request
from .jwt_token import generate_token

import models


def login_view(data):
    input_data = data
    login = input_data['Login']
    password = input_data['password']
    user = config.SESSION.query(models.Employee).filter_by(Login=login).first()

    token = ''
    if user and password == user.Password:
        token = generate_token(user.Login, config.jwt_secret_key)
        result = {
            'code': 'success',
            'token': token
        }
    else:
        result = {
            'code': 'fail',
            'token': token
        }
    return jsonify(result)
