from typing import Tuple
from flask import request, jsonify, abort
from flask.views import MethodView
from marshmallow import ValidationError
from ..helpers import get_request_filter
from ..schemas import UserSchema, UserAuthSchema


class UserResource(MethodView):

    def __init__(self, resolver) -> None:
        self.auth_coordinator = resolver['AuthCoordinator']
        self.tenant_supplier = resolver['TenantSupplier']
        self.authark_reporter = resolver['AutharkReporter']

    def get(self):
        """
        ---
        summary: Return all users.
        tags:
          - Users
        responses:
          200:
            description: "Successful response"
            content:
              application/json:
                schema:
                  type: array
                  items:
                    $ref: '#/components/schemas/User'
        """

        domain, limit, offset = get_request_filter(request)

        users = UserSchema().dump(
            self.authark_reporter.search_users(
                domain), many=True)

        return jsonify(users)

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
        data = str(request.data, encoding='utf8')
        user_registration_dict = UserAuthSchema().loads(data)
        tenant = user_registration_dict['tenant']
        tenants = self.tenant_supplier.search_tenants([('slug', '=', tenant)])

        user = self.auth_coordinator.register(user_registration_dict)

        response = 'Account Created: username<{0}> - email<{1}>'.format(
            user.get('username'), user.get('email'))

        return response, 201
