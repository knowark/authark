from typing import Any, Dict, Tuple
from flask import request
from flask_restful import Resource
from ...schemas import UserSchema


class UserResource(Resource):

    def __init__(self, **kwargs: Any) -> None:
        self.auth_coordinator = kwargs['AuthCoordinator']
        self.spec = kwargs['spec']

    def post(self) -> Tuple[str, int]:
        """
        ---
        summary: Register user.
        tags:
          - Users
        requestBody:
          description: Optional description in *Markdown*
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

        raise ValueError('Yuhuuuu')

        user = self.auth_coordinator.register(data)

        response = 'Account Created: username<{0}> - email<{1}>'.format(
            user.get('username'), user.get('email'))

        return response, 201
