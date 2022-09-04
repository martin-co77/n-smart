from functools import wraps
import jwt as jwt
from flask import request
from config import AppConfig
from exception.auth import AuthException
from services.response import Response


class Authorizer:
    @staticmethod
    def validate_token(token):
        data = jwt.decode(token, AppConfig.AUTH_TOKEN_SECRET, algorithms=["HS256"])
        if data is not None and 'user' in data:
            return data

        raise AuthException('Invalid token', [])

    @staticmethod
    def token_authorizer(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = None
            response = Response()
            if 'Authorization' in request.headers:
                token = request.headers['Authorization'].split(" ")[1]
            if not token:
                return response.set("Invalid token", False, 401).jsonify()
            try:
                data = Authorizer.validate_token(token)
                return f(*args, current_user=data['user'], **kwargs)

            except AuthException as e:
                return response.set('Something went wrong', False, 500)

        return decorated

    @staticmethod
    def webhook_authorizer(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            response = Response()
            token = None
            if 'Authorization' in request.headers:
                token = request.headers['Authorization']

            if 'token' in request.args:
                token = request.args.get('token')

            if not token:
                return response.set('Invalid authorization', False, 401).jsonify()

            if token == AppConfig.WEBHOOK_TOKEN:
                return f(*args, 0, **kwargs)

            data = Authorizer.validate_token(token)
            return f(*args, data['user'], **kwargs)

        return decorated
