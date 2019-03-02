from .development_config import DevelopmentConfig


class ProductionConfig(DevelopmentConfig):
    def __init__(self):
        super().__init__()
        self['mode'] = 'PROD'
        self['gunicorn'].update({
            'debug': True,
            'accesslog': '-',
            'loglevel': 'debug'
        })
        self['database'] = {
            'type': 'json',
            'url': './authark_data.json'
        }
        self['factory'] = 'JsonFactory'
        self['providers'].update({
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
            "AccessTokenService": {
                "method": "pyjwt_access_token_service"
            },
            "RefreshTokenService": {
                "method": "pyjwt_refresh_token_service"
            },
            "ImportService": {
                "method": "json_import_service"
            }
        })
