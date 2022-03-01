from functools import wraps
from http import HTTPStatus

from flask import (
    Response,
    request,
)

from src import BaseConfig


def token_required(func):
    @wraps(func)
    def decorator(*args, **kwargs):
        token = request.headers.get('x-api-key')
        if not token:
            return Response(
                {'message': 'a valid token is missing'},
                status=HTTPStatus.FORBIDDEN,
            )
        if token != BaseConfig.SECRET_KEY:
            return Response(
                {'message': 'token is invalid'},
                status=HTTPStatus.FORBIDDEN,
            )
        return func(*args, **kwargs)

    return decorator
