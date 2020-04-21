check = {
    # # --- PROVIDERS ---
    # "TenantProvider": {
    #     "method": "check_tenant_provider"
    # },
    # # --- SUPPLIERS ---
    # "TenantSupplier": {
    #     "method": "check_tenant_supplier"
    # },
    "JwtSupplier": {
        "method":  "jwt_supplier"
    },
    # --- AUTH ---
    "Authenticate": {
        "method": "middleware_authenticate"
    }
}
