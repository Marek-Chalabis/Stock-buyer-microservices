from functools import wraps
from typing import Callable

from flask import (
    Response,
    request,
)

from src import BaseConfig


def token_required(func: Callable):
    @wraps(func)
    def decorator(*args, **kwargs):
        token = None
        if 'x-api-key' in request.headers:
            token = request.headers.get('x-api-key')
        if not token:
            return Response({'message': 'a valid token is missing'}, status=403)
        if token != BaseConfig.SECRET_KEY:
            return Response({'message': 'token is invalid'}, status=403)
        return func(*args, **kwargs)

    return decorator
