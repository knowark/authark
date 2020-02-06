from pathlib import Path
from .development_config import DevelopmentConfig


class ProductionConfig(DevelopmentConfig):
    def __init__(self):
        super().__init__()
        self['mode'] = 'PROD'
        self['gunicorn'].update({
            'limit_request_line': 0,
            'debug': True,
            'accesslog': '-',
            'loglevel': 'debug'
        })
        self['tenancy'] = {
            'json': Path.home() / 'tenants.json'
        }
        self['data'] = {
            "json": {
                "default": str(Path.home() / 'data')
            }
        }
        self['export'] = {
            'type': 'json',
            'dir': Path.home() / 'export'
        }
        self['factory'] = 'HttpFactory'
        self['strategy'].update({
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
            "ExportService": {
                "method": "json_export_service"
            },
            "CatalogService": {
                "method": "json_catalog_service"
            },
            "ProvisionService": {
                "method": "json_provision_service"
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
        })
