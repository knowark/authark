from flask import Flask
from flask_restful import Api
from authark.app.coordinators.auth_coordinator import AuthCoordinator
from authark.infra.db.memory_user_repository import MemoryUserRepository
from authark.infra.web.resources import AuthResource


def set_routes(app: Flask) -> None:

    @app.route('/')
    def index() -> str:
        return "Welcome to Authark!"

    # Create restful API
    api = Api(app)

    # Auth resource
    user_repository = MemoryUserRepository()
    auth_coordinator = AuthCoordinator(user_repository)

    api.add_resource(
        AuthResource,
        '/auth', '/login',
        resource_class_kwargs={
            'auth_coordinator': auth_coordinator
        })
