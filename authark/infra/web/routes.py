from flask import Flask
from flask_restful import Api
from authark.app.coordinators.auth_coordinator import AuthCoordinator
from authark.app.repositories.user_repository import MemoryUserRepository
from authark.infra.web.resources.auth_resource import AuthResource
from authark.infra.web.resources.register_resource import RegisterResource
from authark.infra.crypto.pyjwt_token_service import PyJWTTokenService
from authark.infra.config.registry import Registry


def set_routes(app: Flask, registry: Registry) -> None:

    @app.route('/')
    def index() -> str:
        return "Welcome to Authark!"

    # Restful API
    api = Api(app)

    # Services
    auth_coordinator = registry['auth_coordinator']

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
