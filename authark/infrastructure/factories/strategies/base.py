base = {
    # --- PARSER ---
    "QueryParser": {
        "method": "query_parser"
    },
    # --- PROVIDERS ---
    "TenantProvider": {
        "method": "standard_tenant_provider"
    },
    # --- REPOSITORIES ---
    "CredentialRepository": {
        "method": "memory_credential_repository"
    },
    "DominionRepository": {
        "method": "memory_dominion_repository"
    },
    "RankingRepository": {
        "method": "memory_ranking_repository"
    },
    "RoleRepository": {
        "method": "memory_role_repository"
    },
    "UserRepository": {
        "method": "memory_user_repository"
    },
    # --- SERVICES ---
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
    "ProvisionService": {
        "method": "memory_provision_service"
    },
    "AccessService": {
        "method": "access_service"
    },
    # --- COORDINATORS ---
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
    # --- INFORMERS ---
    "AutharkInformer": {
        "method": "standard_authark_informer"
    },
    "ComposingInformer": {
        "method": "standard_composing_informer"
    },
    # --- SUPPLIERS ---
    "TenantSupplier": {
        "method": "memory_tenant_supplier"
    }
}
