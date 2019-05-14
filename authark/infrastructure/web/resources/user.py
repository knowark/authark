from typing import Tuple
from flask import request, jsonify, abort
from flask.views import MethodView
from marshmallow import ValidationError
from ..schemas import UserSchema


class UserResource(MethodView):

    def __init__(self, resolver) -> None:
        self.auth_coordinator = resolver['AuthCoordinator']
        self.tenant_supplier = resolver['TenantSupplier']

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

        user_registration_dict = UserSchema().loads(request.data)
        tenant = user_registration_dict['tenant']
        tenants = self.tenant_supplier.search_tenants([('slug', '=', tenant)])
        if not tenants:
            abort(400, f"Tenant '{tenant}' not found.")

        user = self.auth_coordinator.register(user_registration_dict)

        response = 'Account Created: username<{0}> - email<{1}>'.format(
            user.get('username'), user.get('email'))

        return response, 201
