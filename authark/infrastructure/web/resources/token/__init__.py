from typing import Any, Dict, Tuple
from flask import request
from flask_restful import Resource
from flasgger import swag_from


class TokenResource(Resource):

    def __init__(self, **kwargs: Any) -> None:
        self.auth_coordinator = kwargs['AuthCoordinator']

    def get(self) -> str:
        return "Authentication endpoint. Please 'Post' to '/auth'"

    @swag_from('post.yml')
    def post(self) -> Tuple[str, int]:
        data = request.get_json()
        try:
            if 'refresh_token' in data:
                tokens = self.auth_coordinator.refresh_authenticate(
                    data['refresh_token'])
            else:
                username = data.get('username')
                password = data.get('password')
                client = data.get('client')
                tokens = self.auth_coordinator.authenticate(
                    username, password, client)
        except Exception as e:
            return str(e), 401

        return tokens, 200