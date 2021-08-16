from .views import *
from .jwt_token import *

"""Authentication utilities"""
from dataclasses import dataclass, field
from functools import wraps
from flask import request, g

import config
from models import Employee
from permissions import Authority


@dataclass
class AuthenticationError(Exception):

    def __init__(
            self,
            status_code: int = field(default=403),
            error_code: str = field(default="invalid-token"),
            message: str = field(default="The provided auth token is invalid")
    ):
        super().__init__(status_code, error_code, message)


def get_token_auth_header():
    auth = request.headers.get("Authorization", None)
    if not auth:
        raise AuthenticationError(error_code="authorization_header_missing", message="Authorization header is expected", status_code=401)

    parts = auth.split()

    if parts[0].lower() != "bearer":
        raise AuthenticationError(error_code="invalid-header",message="Authorization header must start with Bearer", status_code=401)
    elif len(parts) == 1:
        raise AuthenticationError(error_code="invalid-header", message="Token not found", status_code=401)
    elif len(parts) > 2:
        raise AuthenticationError(error_code="invalid-header", message="Authorization header must be Bearer token", status_code=401)

    token = parts[1]
    return token
