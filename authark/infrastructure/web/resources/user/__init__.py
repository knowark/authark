from typing import Any, Dict, Tuple
from flask import request
from flask_restful import Resource
from flasgger import swag_from


class UserResource(Resource):

    def __init__(self, **kwargs: Any) -> None:
        self.auth_coordinator = kwargs['AuthCoordinator']

    @swag_from('post.yml')
    def post(self) -> Tuple[str, int]:
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        user = self.auth_coordinator.register(username, email, password)

        response = 'Account Created: username<{0}> - email<{1}>'.format(
            username, email)

        return response, 201
