from typing import Any, Dict, Tuple
from flask import request
from flask_restful import Resource


class AuthResource(Resource):

    def __init__(self, **kwargs: Any) -> None:
        self.auth_coordinator = kwargs['auth_coordinator']

    def get(self) -> Dict[str, str]:
        authenticated = self.auth_coordinator.authenticate(
            "Esteban", "Echeverry")

        return {
            'extra': 'happy',
            'authenticated': authenticated
        }

    def post(self) -> Tuple[str, int]:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        try:
            token = self.auth_coordinator.authenticate(username, password)
        except Exception as e:
            return '', 401

        return token.value, 200
