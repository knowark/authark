from typing import Any, Dict, Tuple
from flask import request
from flask.views import MethodView
from ..schemas import UserSchema


class UserResource(MethodView):

    def __init__(self, registry) -> None:
        self.auth_coordinator = registry['AuthCoordinator']
        self.spec = registry['spec']

    def post(self) -> Tuple[str, int]:
        """
        ---
        summary: Register user.
        tags:
          - Users
        requestBody:
          required: true
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'
        responses:
          201:
            description: "User created"
        """

        print('REQUEST >>>>', request, request.data)
        print('JSON', request.get_json())
        data = UserSchema().loads(request.data).data

        print('DATA>>>>', request, request.data, data)

        user = self.auth_coordinator.register(data)

        response = 'Account Created: username<{0}> - email<{1}>'.format(
            user.get('username'), user.get('email'))

        return response, 201
