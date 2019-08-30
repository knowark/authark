import inspect
from pytest import fixture
from injectark import Injectark
from authark.infrastructure.core import Config, build_factory, Factory


@fixture
def mock_config():
    class MockConfig(Config):
        def __init__(self):
            self['factory'] = 'MemoryFactory'
            self['authorization'] = {
                "dominion": "proser"
            }

    return MockConfig()


@fixture
def mock_strategy():
    return {
        "ExpressionParser": {
            "method": "expression_parser"
        },
        "UserRepository": {
            "method": "memory_user_repository"
        },
        "CredentialRepository": {
            "method": "memory_credential_repository"
        },
        "DominionRepository": {
            "method": "memory_dominion_repository"
        },
        "GrantRepository": {
            "method": "memory_grant_repository"
        },
        "RoleRepository": {
            "method": "memory_role_repository"
        },
        "RankingRepository": {
            "method": "memory_ranking_repository"
        },
        "PolicyRepository": {
            "method": "memory_policy_repository"
        },
        "ResourceRepository": {
            "method": "memory_resource_repository"
        },
        "PermissionRepository": {
            "method": "memory_permission_repository"
        },
        "HashService": {
            "method": "memory_hash_service"
        },
        "AccessTokenService": {
            "method": "memory_access_token_service"
        },
        "RefreshTokenService": {
            "method": "memory_refresh_token_service"
        },
        "ImportService": {
            "method": "memory_import_service"
        },
        "TenantProvider": {
            "method": "standard_tenant_provider"
        },
        "AccessService": {
            "method": "access_service"
        },
        "AuthCoordinator": {
            "method": "auth_coordinator"
        },
        "ManagementCoordinator": {
            "method": "management_coordinator"
        },
        "ImportCoordinator": {
            "method": "import_coordinator"
        },
        "AssignmentCoordinator": {
            "method": "assignment_coordinator"
        },
        "SessionCoordinator": {
            "method": "session_coordinator"
        },
        "AutharkReporter": {
            "method": "standard_authark_reporter"
        },
        "ComposingReporter": {
            "method": "standard_composing_reporter"
        },
        "TenantSupplier": {
            "method": "memory_tenant_supplier"
        }
    }


def test_memory_factory(mock_config, mock_strategy):
    factory = build_factory(mock_config)
    resolver = Injectark(strategy=mock_strategy, factory=factory)

    for resource in mock_strategy.keys():
        result = resolver.resolve(resource)
        classes = inspect.getmro(type(result))
        assert resource in [item.__name__ for item in classes]
