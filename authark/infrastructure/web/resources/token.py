from typing import Any, Dict, Tuple
from flask import request
from flask.views import MethodView


class TokenResource(MethodView):

    def __init__(self, registry) -> None:
        self.auth_coordinator = registry['AuthCoordinator']
        self.spec = registry['spec']

    def get(self) -> str:
        return "Authentication endpoint. Please 'Post' to '/auth'"

    def post(self) -> Tuple[str, int]:
        """
        ---
        summary: Request token.
        tags:
          - Tokens
        requestBody:
          required: true
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/TokenRequest'
        responses:
          201:
            description: "Token created"
            content:
              application/json:
                schema:
                  $ref: "#/components/schemas/Token"
        """
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
