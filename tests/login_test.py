import json


def login_as_admin():
    payload = json.dumps({
        "Login": 'Super_admin',
        "password": '12345678'
    })
    return payload


def login_as_head_of_company():
    payload = json.dumps({
        "Login": "Head_of_company",
        "password": "12345678"
    })
    return payload


def login_as_head_of_department():
    payload = json.dumps({
        "Login": "Head_of_department",
        "password": "12345678"
    })
    return payload


def login_as_user():
    payload = json.dumps({
        "Login": "User",
        "password": "12345678"
    })
    return payload
