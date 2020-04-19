from .config import Config


class DevelopmentConfig(Config):
    def __init__(self):
        super().__init__()
        self['mode'] = 'DEV'
        self['gunicorn'].update({
            'debug': True,
            'accesslog': '-',
            'loglevel': 'debug'
        })
        self['factory'] = 'MemoryFactory'
        self['strategy'] = {
            "QueryParser": {
                "method": "query_parser"
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
            "RoleRepository": {
                "method": "memory_role_repository"
            },
            "RankingRepository": {
                "method": "memory_ranking_repository"
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
            "CatalogService": {
                "method": "memory_catalog_service"
            },
            "TenantProvider": {
                "method": "standard_tenant_provider"
            },
            "ProvisionService": {
                "method": "memory_provision_service"
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
