from typing import Callable
from functools import wraps
from flask import request
from ....application.coordinators import SessionCoordinator
from ...core import JwtSupplier, AuthenticationError, TenantSupplier
from ..schemas import UserSchema


class Authenticate:

    def __init__(self, tenant_supplier: TenantSupplier,
                 session_coordinator: SessionCoordinator) -> None:
        self.tenant_supplier = tenant_supplier
        self.session_coordinator = session_coordinator

    def __call__(self, method: Callable) -> Callable:
        @wraps(method)
        def decorator(*args, **kwargs):
            tenant_id = request.headers.get('TenantId')
            user_id = request.headers.get('UserId')
            email = request.headers.get('From', "@")
            name = email.split('@')[0]
            roles = request.headers.get('Roles', '').strip().split(',')

            user_dict = {
                'id': user_id,
                'name': name,
                'email': email,
                'roles': roles
            }
            # self.session_coordinator.set_user(user_dict)

            tenant_dict = self.tenant_supplier.get_tenant(tenant_id)
            self.session_coordinator.set_tenant(tenant_dict)

            return method(*args, **kwargs)

        return decorator


# class Authenticate:

#     def __init__(self, jwt_supplier: JwtSupplier,
#                  tenant_supplier: TenantSupplier,
#                  session_coordinator: SessionCoordinator) -> None:
#         self.jwt_supplier = jwt_supplier
#         self.tenant_supplier = tenant_supplier
#         self.session_coordinator = session_coordinator

#     def __call__(self, method: Callable) -> Callable:
#         @wraps(method)
#         def decorator(*args, **kwargs):
#             authorization = request.headers.get('Authorization', "")
#             token = authorization.replace('Bearer ', '')
#             if not token:
#                 token = request.args.get('access_token')
#             try:
#                 token_payload = self.jwt_supplier.decode(
#                     token, verify=False)

#                 tenant_dict = self.tenant_supplier.get_tenant(
#                     token_payload['tid'])

#                 # secret = tenant_dict['secret']

#                 token_payload = self.jwt_supplier.decode(token, secret=None)
#                 self.session_coordinator.set_tenant(tenant_dict)

#                 user_dict = UserSchema().load(token_payload)
#                 # self.session_coordinator.set_user(user_dict)
#             except Exception as e:
#                 raise AuthenticationError(
#                     "Couldn't authenticate the request.")

#             return method(*args, **kwargs)

#         return decorator
