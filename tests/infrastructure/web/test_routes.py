import json
import jwt
from pytest import fixture
from flask import Flask
from injectark import Injectark
from authark.application.models import (
    User, Credential, Dominion, Role, Ranking)
from authark.application.repositories import (
    ExpressionParser,
    MemoryUserRepository, MemoryCredentialRepository,
    MemoryDominionRepository, MemoryRoleRepository,
    MemoryRankingRepository)
from authark.application.coordinators import AuthCoordinator
from authark.application.services import (
    MemoryHashService, StandardAccessService)
from authark.infrastructure.web.base import create_app
from authark.infrastructure.config import TrialConfig
from authark.infrastructure.factories import build_factory
from authark.infrastructure.crypto import (
    PyJWTRefreshTokenService, PyJWTAccessTokenService)


@fixture
def resolver():
    parser = ExpressionParser()
    user_repository = MemoryUserRepository(parser)
    credential_repository = MemoryCredentialRepository(parser)
    user_repository.load({
        '1': User(
            id="1",
            username="eecheverry",
            email="eecheverry@nubark.com"),
        '2': User(
            id="2",
            username="mvivas",
            email="mvivas@gmail.com"
        )
    })
    refresh_token = jwt.encode(
        {'user': "pepe"}, 'REFRESHSECRET').decode('utf-8')
    credential_repository.load({
        "1": Credential(id='1', user_id='1', value="HASHED: ABC1234"),
        "2": Credential(id='2', user_id='2', value="HASHED: XYZ098"),
        "3": Credential(id='3', user_id='1', value=refresh_token,
                        type='refresh_token'),
    })
    ranking_repository = MemoryRankingRepository(parser)
    ranking_repository.load({
        "1": Ranking(id='1', user_id='1', role_id='1',
                        description="Service's Administrator")
    })
    role_repository = MemoryRoleRepository(parser)
    role_repository.load({
        "1": Role(id='1', name='admin', dominion_id='1',
                  description="Service's Administrator")
    })
    dominion_repository = MemoryDominionRepository(parser)
    dominion_repository.load({
        "1": Dominion(id='1', name='Data Server',
                      url="https://dataserver.nubark.com")
    })
    access_token_service = PyJWTAccessTokenService(
        'TESTSECRET', 'HS256', 3600)
    access_service = StandardAccessService(
        ranking_repository, role_repository,
        dominion_repository, access_token_service)

    refresh_token_service = PyJWTRefreshTokenService(
        'REFRESHSECRET', 'HS256', 3600, 3600)
    hash_service = MemoryHashService()
    auth_coordinator = AuthCoordinator(
        user_repository, credential_repository,
        hash_service, access_service,
        refresh_token_service)

    resolver = Injectark()

    config = TrialConfig()
    factory = build_factory(config)
    strategy = config['strategy']

    resolver = Injectark(strategy=strategy, factory=factory)

    resolver.registry['AuthCoordinator'] = auth_coordinator

    return resolver


@fixture
def app(resolver) -> Flask:
    """Create app testing client"""
    config = TrialConfig()

    app = create_app(config=config, resolver=resolver)
    app.testing = True
    app = app.test_client()

    return app


def test_auth_get_route(app: Flask) -> None:
    response = app.get('/auth')
    expected_response = (b"Authentication endpoint. "
                         b"Please 'Post' to '/auth'")
    assert expected_response in response.get_data()


def test_auth_post_route_failed_authentication(app: Flask) -> None:
    response = app.post(
        '/auth',
        data=json.dumps(dict(
            username="eecheverry",
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
            password="ABC1234",
            # client="mobile"
        )),
        content_type='application/json')
    assert response.status_code == 200
    data = response.get_data()
    assert len(data) > 0


def test_auth_post_route_with_refresh_token(app: Flask) -> None:
    token = jwt.encode(
        {'user': "pepe"}, 'REFRESHSECRET').decode('utf-8')
    response = app.post(
        '/auth',
        data=json.dumps(dict(
            refresh_token=token
        )),
        content_type='application/json')
    assert response.status_code == 200
    data = response.get_data()
    assert len(data) > 0


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
