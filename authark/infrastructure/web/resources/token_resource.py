from typing import Any, Dict, Tuple
from flask import request
from flask_restful import Resource


class TokenResource(Resource):

    def __init__(self, **kwargs: Any) -> None:
        self.auth_coordinator = kwargs['auth_coordinator']

    def get(self) -> str:
        return "Authentication endpoint. Please 'Post' to '/auth'"

    def post(self) -> Tuple[str, int]:
        data = request.get_json()
        try:
            username = data.get('username')
            password = data.get('password')
            token = self.auth_coordinator.authenticate(username, password)
        except Exception as e:
            return '', 401

        return str(token.value), 200
