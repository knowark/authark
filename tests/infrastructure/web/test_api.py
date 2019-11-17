import json
import jwt
from pytest import fixture, raises
from flask import Flask
from injectark import Injectark
from authark.application.models import (
    User, Credential, Dominion, Role, Ranking,
    Resource, Grant, Policy, Permission)
from authark.application.utilities import (
    ExpressionParser, StandardTenantProvider, Tenant)
from authark.application.repositories import (
    MemoryUserRepository, MemoryCredentialRepository,
    MemoryDominionRepository, MemoryRoleRepository,
    MemoryRankingRepository, MemoryResourceRepository,
    MemoryGrantRepository, MemoryPermissionRepository,
    MemoryPolicyRepository)
from authark.application.services import MemoryHashService, AccessService
from authark.application.coordinators import (
    AuthCoordinator, SessionCoordinator)
from authark.application.reporters import StandardAutharkReporter
from authark.infrastructure.web.base import create_app
from authark.infrastructure.core import (
    TrialWebConfig, build_factory, PyJWTRefreshTokenService,
    PyJWTAccessTokenService, AuthenticationError)


# Fixtures

@fixture
def resolver():
    parser = ExpressionParser()
    tenant = Tenant(id='1', name="Default", location="default")
    tenant_provider = StandardTenantProvider(tenant)
    user_repository = MemoryUserRepository(parser, tenant_provider)
    credential_repository = MemoryCredentialRepository(parser, tenant_provider)
    user_repository.load({
        "default": {
            '1': User(
                id="1",
                username="eecheverry",
                email="eecheverry@nubark.com"),
            '2': User(
                id="2",
                username="mvivas",
                email="mvivas@gmail.com")
        }
    })
    refresh_token = jwt.encode(
        {'user': "pepe"}, 'REFRESHSECRET').decode('utf-8')
    credential_repository.load({
        "default": {
            "1": Credential(id='1', user_id='1', value="HASHED: ABC1234"),
            "2": Credential(id='2', user_id='2', value="HASHED: XYZ098"),
            "3": Credential(id='3', user_id='1', value=refresh_token,
                            type='refresh_token'),
        }

    })
    ranking_repository = MemoryRankingRepository(parser, tenant_provider)
    ranking_repository.load({
        "default": {
            "1": Ranking(id='1', user_id='1', role_id='1',
                         description="Service's Administrator")
        }
    })
    role_repository = MemoryRoleRepository(parser, tenant_provider)
    role_repository.load({
        "default": {
            "1": Role(id='1', name='admin', dominion_id='1',
                      description="Service's Administrator")
        }
    })
    dominion_repository = MemoryDominionRepository(parser, tenant_provider)
    dominion_repository.load({
        "default": {
            "1": Dominion(id='1', name='Data Server',
                          url="https://dataserver.nubark.com")
        }
    })
    resource_repository = MemoryResourceRepository(parser, tenant_provider)
    resource_repository.load({
        "default": {
            "1": Resource(id='1', name='employees',
                          dominion_id='1')
        }
    })
    grant_repository = MemoryGrantRepository(parser, tenant_provider)
    grant_repository.load({
        "default": {
            '001': Grant(id='001', permission_id='001', role_id='1')
        }
    })
    permission_repository = MemoryPermissionRepository(parser, tenant_provider)
    permission_repository.load({
        "default": {
            "001": Permission(id='001', policy_id='001', resource_id='1')
        }
    })
    policy_repository = MemoryPolicyRepository(parser, tenant_provider)
    policy_repository.load({
        "default": {
            "001": Policy(id='001', name='First Role Only', value="1")
        }
    })

    access_token_service = PyJWTAccessTokenService(
        'TESTSECRET', 'HS256', 3600)

    access_service = AccessService(
        ranking_repository, role_repository,
        dominion_repository, resource_repository,
        grant_repository, permission_repository,
        policy_repository, access_token_service,
        tenant_provider)

    refresh_token_service = PyJWTRefreshTokenService(
        'REFRESHSECRET', 'HS256', 3600, 3600)
    hash_service = MemoryHashService()
    auth_coordinator = AuthCoordinator(
        user_repository, credential_repository,
        dominion_repository,
        hash_service, access_service,
        refresh_token_service)

    session_coordinator = SessionCoordinator(tenant_provider)

    authark_reporter = StandardAutharkReporter(
        user_repository=user_repository,
        credential_repository=credential_repository,
        dominion_repository=dominion_repository,
        role_repository=role_repository,
        policy_repository=policy_repository,
        resource_repository=resource_repository
    )

    resolver = Injectark()

    config = TrialWebConfig()
    factory = build_factory(config)
    strategy = config['strategy']

    resolver = Injectark(strategy=strategy, factory=factory)

    resolver.registry['AuthCoordinator'] = auth_coordinator
    resolver.registry['SessionCoordinator'] = session_coordinator
    resolver['TenantSupplier'].arranger.cataloguer.catalog = {
        "1": tenant
    }
    resolver.registry['AutharkReporter'] = authark_reporter

    return resolver


@fixture
def app(resolver) -> Flask:
    """Create app testing client"""
    config = TrialWebConfig()

    app = create_app(config=config, resolver=resolver)
    app.testing = True
    app = app.test_client()

    return app


@fixture
def headers() -> dict:

    payload_dict = {
        "tid": "1", "uid": "1", "name": "eecheverry",
        "email": "eecheverry@nubark.com"}

    return {
        "Authorization":  (jwt.encode(payload_dict, "DEVSECRET123",
                                      algorithm='HS256').decode('utf-8')),
        "From": "eecheverry@nubark.com",
        "TenantId": "1",
        "UserId": "1",
        "Roles": ["user"]

    }

# General tests


def test_root_resource(app: Flask) -> None:
    response = app.get('/')
    data = str(response.data, 'utf-8')
    assert data is not None


def test_root_resource_request_none(app: Flask) -> None:
    response = app.get('/?api')
    data = str(response.data, 'utf-8')
    assert data is not None


# Tokens resource tests


def test_auth_get_route(app: Flask) -> None:
    response = app.get('/auth')
    expected_response = (b"Authentication endpoint. "
                         b"Please 'Post' to '/auth'")
    assert expected_response in response.get_data()


def test_auth_post_route_failed_authentication(app: Flask) -> None:
    response = app.post(
        '/auth',
        data=json.dumps(dict(
            tenant="default",
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
            tenant="default",
            username="eecheverry",
            password="ABC1234",
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
            tenant="default",
            refresh_token=token
        )),
        content_type='application/json')
    assert response.status_code == 200
    data = response.get_data()
    assert len(data) > 0

# Users resource tests


def test_get_users(app: Flask, headers: dict) -> None:
    response = app.get(
        '/register?filter=[["id", "=", "1"]]', headers=headers)
    assert response.status_code == 200
    assert len(json.loads(str(response.data, 'utf-8'))) == 1


def test_get_filter_error(app: Flask, headers: dict) -> None:
    response = app.get(
        '/register?filter=[** BAD FILTER **]', headers=headers)
    assert response.status_code == 200
    assert len(json.loads(str(response.data, 'utf-8'))) == 2


def test_register_post_route(app: Flask, headers: dict) -> None:
    response = app.post(
        '/register',
        data=json.dumps(dict(
            tenant="default",
            username="gecheverry",
            email="gecheverry@gmail.com",
            password="POI123"
        )),
        content_type='application/json',
        headers=headers)

    assert response.status_code == 201
    assert b"username<gecheverry>" in response.get_data()
    assert b"email<gecheverry@gmail.com>" in response.get_data()
