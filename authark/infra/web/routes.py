from flask import Flask
from flask_restful import Api
from authark.app.coordinators.auth_coordinator import AuthCoordinator
from authark.infra.db.memory_user_repository import MemoryUserRepository
from authark.infra.web.resources.auth_resource import AuthResource
from authark.infra.web.resources.register_resource import RegisterResource
from authark.infra.crypto.pyjwt_token_service import PyJWTTokenService


def set_routes(app: Flask) -> None:

    @app.route('/')
    def index() -> str:
        return "Welcome to Authark!"

    # Restful API
    api = Api(app)

    # Services
    user_repository = MemoryUserRepository()
    token_service = PyJWTTokenService('DEVSECRET123', 'HS256')
    auth_coordinator = AuthCoordinator(user_repository, token_service)

    # Auth resource
    api.add_resource(
        AuthResource,
        '/auth', '/login', '/token',
        resource_class_kwargs={
            'auth_coordinator': auth_coordinator
        })

    # Register resource
    api.add_resource(
        RegisterResource,
        '/register', '/signup',
        resource_class_kwargs={
            'auth_coordinator': auth_coordinator
        })
