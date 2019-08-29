import json
from authark.infrastructure.core.tenancy import JsonTenantSupplier
from pathlib import Path


def test_json_tenant_supplier_instantiation(json_tenant_supplier):
    isinstance(json_tenant_supplier, JsonTenantSupplier)


def test_json_tenant_supplier_tenant_creation(
        json_tenant_supplier, tenant_dict, directory_data):
    json_tenant_supplier.create_tenant(tenant_dict)

    with open(directory_data / "tenants.json", 'r') as catalog:
        data = catalog.read()

    catalog_data = json.loads(data)

    assert len(catalog_data["tenants"]) == 1
