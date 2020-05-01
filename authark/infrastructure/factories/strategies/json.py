json = {
    # --- REPOSITORIES ---
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
    # --- SERVICES ---
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
    # --- SUPPLIERS ---
    "TenantSupplier": {
        "method": "json_tenant_supplier"
    },
    "JwtSupplier": {
        "method":  "jwt_supplier"
    },
    # --- AUTH ---
    "Authenticate": {
        "method": "middleware_authenticate"
    }
}