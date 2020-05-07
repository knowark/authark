from functools import partial
from injectark import Injectark
from ..schemas import UserSchema
from .resource import Resource


class UserResource(Resource):
    def __init__(self, injector: Injectark) -> None:
        informer = injector['AutharkInformer']
        manager = injector['AuthManager']

        super().__init__(
            UserSchema,
            partial(informer.count, 'user'),
            partial(informer.search, 'user'),
            manager.register,
            manager.deregister)


# class UserResource:

#     def __init__(self, resolver) -> None:
#         self.auth_coordinator = resolver['AuthCoordinator']
#         self.tenant_supplier = resolver['TenantSupplier']
#         self.authark_reporter = resolver['AutharkReporter']

#     def head(self) -> int:
#         """
#         ---
#         summary: Return users headers.
#         tags:
#           - Users
#         """
#         # domain, _, _ = get_request_filter(request)

#         # response = make_response()
#         # response.headers['Total-Count'] = len(
#         #     self.authark_reporter.search_users(domain, None, None))

#         # return response
#         return 0

#     def get(self):
#         """
#         ---
#         summary: Return all users.
#         tags:
#           - Users
#         responses:
#           200:
#             description: "Successful response"
#             content:
#               application/json:
#                 schema:
#                   type: array
#                   items:
#                     $ref: '#/components/schemas/User'
#         """

#         # domain, limit, offset = get_request_filter(request)

#         # users = UserSchema().dump(
#         #     self.authark_reporter.search_users(
#         #         domain, limit, offset), many=True)

#         # return jsonify(users)
#         return None

#     def post(self) -> None:
#         """
#         ---
#         summary: Register user.
#         tags:
#           - Users
#         requestBody:
#           required: true
#           content:
#             application/json:
#               schema:
#                 $ref: '#/components/schemas/User'
#         responses:
#           201:
#             description: "User created"
#         """
#         # data = str(request.data, encoding='utf8')
#         # user_registration_dict = UserAuthSchema().loads(data)
#         # tenant = user_registration_dict['tenant']
#         # tenants = self.tenant_supplier.search_tenants([('slug', '=', tenant)])

#         # user = self.auth_coordinator.register(user_registration_dict)

#         # response = 'Account Created: username<{0}> - email<{1}>'.format(
#         #     user.get('username'), user.get('email'))

#         return None
