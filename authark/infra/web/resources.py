from typing import Any
from flask_restful import Resource


class AuthResource(Resource):

    def __init__(self, **kwargs: Any) -> None:
        self.auth_coordinator = kwargs['auth_coordinator']

    def get(self) -> dict:
        authenticated = self.auth_coordinator.authenticate(
            "Esteban", "Echeverry")

        return {
            'extra': 'happy',
            'authenticated': authenticated
        }

    def post(self) -> dict:
        return {"is": "working"}
