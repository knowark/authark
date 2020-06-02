from typing import Dict, Any
from authark.core.suppliers import json_tenant_supplier
from authark.core.suppliers import JsonTenantSupplier


def test_json_tenant_supplier_instantiation(monkeypatch):
    expected = {}

    def mock_resolve_managers(config: Dict[str, Any]):
        nonlocal expected
        expected = config
        return None, None

    monkeypatch.setattr(
        json_tenant_supplier,  'resolve_managers', mock_resolve_managers)
    catalog_path = "tenants.json"
    directory_template = "__template__"
    zones = {
        'default': ""
    }

    tenant_supplier = JsonTenantSupplier(
        catalog_path, zones, directory_template)

    isinstance(tenant_supplier, JsonTenantSupplier)

    assert expected == {
        'cataloguer_kind': 'json',
        'catalog_path': catalog_path,
        'provisioner_kind': 'directory',
        'provision_template': directory_template,
        'provision_directory_zones': zones
    }
