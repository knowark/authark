import json
from pytest import fixture
from flask import Flask
from authark.application.models.user import User
from authark.infrastructure.web.registry import Registry
from authark.infrastructure.web.main import main

from authark.application.coordinators.auth_coordinator import AuthCoordinator
from authark.application.repositories.user_repository import (
    MemoryUserRepository)
from authark.infrastructure.crypto.pyjwt_token_service import PyJWTTokenService


class MockRegistry(Registry):

    def __init__(self) -> None:
        user_repository = MemoryUserRepository()
        user_repository.load({
            'eecheverry': User(
                "eecheverry",
                "eecheverry@nubark.com",
                "ABC1234"),
            'mvivas': User(
                "mvivas",
                "mvivas@gmail.com",
                "XYZ098"
            )
        })
        token_service = PyJWTTokenService('TESTSECRET', 'HS256')
        auth_coordinator = AuthCoordinator(user_repository, token_service)

        self['auth_coordinator'] = auth_coordinator


@fixture
def app() -> Flask:
    """Create app testing client"""

    mock_registry = MockRegistry()

    app = main(registry=mock_registry)
    app.testing = True
    app = app.test_client()

    return app


def test_root_route(app: Flask) -> None:
    response = app.get('/')
    assert b"Welcome to Authark" in response.get_data()


def test_auth_get_route(app: Flask) -> None:
    response = app.get('/auth')
    expected_response = (b"Authentication endpoint. "
                         b"Please 'Post' to '/auth'")
    assert expected_response in response.get_data()


def test_auth_post_route_failed_authentication(app: Flask) -> None:
    response = app.post(
        '/auth',
        data=json.dumps(dict(
            username="Esteban",
            password="ABC1234"
        )),
        content_type='application/json')
    expected_response = b''
    assert expected_response in response.get_data()


def test_auth_post_route_successful_authentication(app: Flask) -> None:
    response = app.post(
        '/auth',
        data=json.dumps(dict(
            username="eecheverry",
            password="ABC1234"
        )),
        content_type='application/json')

    assert response.status_code == 200
    assert len(response.get_data()) > 0


def test_register_post_route(app: Flask) -> None:
    response = app.post(
        '/register',
        data=json.dumps(dict(
            username="gecheverry",
            email="gecheverry@gmail.com",
            password="POI123"
        )),
        content_type='application/json')

    assert response.status_code == 201
    assert b"username<gecheverry>" in response.get_data()
    assert b"email<gecheverry@gmail.com>" in response.get_data()
