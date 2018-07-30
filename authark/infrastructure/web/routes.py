from flask import Flask
from flask_restful import Api
from authark.application.coordinators.auth_coordinator import AuthCoordinator
from authark.application.repositories.user_repository import (
    MemoryUserRepository)
from authark.infrastructure.web.resources.token_resource import TokenResource
from authark.infrastructure.web.resources.user_resource import (
    UserResource)
from authark.infrastructure.crypto.pyjwt_token_service import PyJWTTokenService
from authark.infrastructure.config.registry import Registry


def set_routes(app: Flask, registry: Registry) -> None:

    @app.route('/')
    def index() -> str:
        return "Welcome to Authark!"

    # Restful API
    api = Api(app)

    # Services
    auth_coordinator = registry['auth_coordinator']

    # Token resource
    api.add_resource(
        TokenResource,
        '/auth', '/login', '/token',
        resource_class_kwargs={
            'auth_coordinator': auth_coordinator
        })

    # User resource
    api.add_resource(
        UserResource,
        '/register', '/signup',
        resource_class_kwargs={
            'auth_coordinator': auth_coordinator
        })
