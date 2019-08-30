import inspect
from pytest import fixture
from injectark import Injectark
from authark.infrastructure.core import Config, build_factory, factory


@fixture
def mock_config():
    class MockConfig(Config):
        def __init__(self):
            self['factory'] = 'HttpFactory'
            self['authorization'] = {
                "dominion": "proser"
            }
            self['tenancy'] = {
                "json": "/tmp/tenants.json"
            }
            self['data'] = {
                "json": {
                    "default": '/tmp/data'
                }
            }
            self['tokens']={
                'tenant': {
                    "secret": "",
                    "algorithm": "",
                    "lifetime": ""
                },
                'access': {
                    "secret": "",
                    "algorithm": "",
                    "lifetime": ""
                },
                'refresh': {
                    "secret": "",
                    "algorithm": "",
                    "lifetime": "",
                    "threshold": ""
                },
            }

    return MockConfig()


@fixture
def mock_strategy():
    return {
        "TenantProvider": {
            "method": "standard_tenant_provider"
        },
        "ExpressionParser": {
            "method": "expression_parser"
        },
        "UserRepository": {
            "method": "json_user_repository"
        },
        "CredentialRepository": {
            "method": "json_credential_repository"
        },
        "DominionRepository": {
            "method": "json_dominion_repository"
        },
        "RoleRepository": {
            "method": "json_role_repository"
        },
        "RankingRepository": {
            "method": "json_ranking_repository"
        },
        "PolicyRepository": {
            "method": "json_policy_repository"
        },
        "ResourceRepository": {
            "method": "json_resource_repository"
        },
        "GrantRepository": {
            "method": "json_grant_repository"
        },
        "PermissionRepository": {
            "method": "json_permission_repository"
        },
        "HashService": {
            "method": "passlib_hash_service"
        },
        "TokenService": {
            "method": "pyjwt_token_service"
        },
        "AccessTokenService": {
            "method": "pyjwt_access_token_service"
        },
        "RefreshTokenService": {
            "method": "pyjwt_refresh_token_service"
        },
        "ImportService": {
            "method": "json_import_service"
        },
        "SessionCoordinator": {
            "method": "session_coordinator"
        },
        "TenantSupplier": {
            "method": "json_tenant_supplier"
        },
        "JwtSupplier": {
            "method":  "jwt_supplier"
        },
        "Authenticate": {
            "method": "middleware_authenticate"
        }
    }


def test_json_factory(mock_config, mock_strategy):
    factory = build_factory(mock_config)
    resolver = Injectark(strategy=mock_strategy, factory=factory)

    for resource in mock_strategy.keys():
        result = resolver.resolve(resource)
        classes = inspect.getmro(type(result))
        assert resource in [item.__name__ for item in classes]
