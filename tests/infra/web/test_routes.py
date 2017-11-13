import json
from pytest import fixture
from flask import Flask
from authark.infra.web.main import main


@fixture
def app() -> Flask:
    """Create app testing client"""
    app = main()
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
            username="Esteban",
            password="ABC1234"
        )),
        content_type='application/json')
    expected_response = b''
    assert expected_response in response.get_data()
