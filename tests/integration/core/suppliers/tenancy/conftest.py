from pytest import fixture
from json import dump
from pathlib import Path
from authark.integration.core.suppliers import JsonTenantSupplier


@fixture
def catalog_path(tmp_path):
    catalog_path = tmp_path / "tenants.json"
    with open(catalog_path, 'w') as f:
        dump({"tenants": {}}, f, indent=2)
    return catalog_path


@fixture
def zones(tmp_path):
    return {
        "default": {
            "directory": tmp_path
        }
    }


@fixture
def directory_data(tmp_path):
    return tmp_path


@fixture
def directory_template(tmp_path):
    template_path = tmp_path / "__template__"

    Path.mkdir(template_path)

    data = ["credentials", "dominions", "errors",
            "rankings", "resources", "roles", "tokens", "types",
            "users"]

    for model in data:
        with open(template_path / f"{model}.json", 'w') as f:
            dump({model: {}}, f, indent=2)

    return "__template__"


@fixture
def tenant_dict():
    return {
        "id": "c5934df0-cab9-4660-af14-c95272a92ab7",
        "name": "Servagro",
        "email": "",
        "active": True,
        "slug": "servagro",
        "attributes": {},
        "zone": "default",
    }


@fixture
def json_tenant_supplier(catalog_path, zones, directory_template):
    return JsonTenantSupplier(catalog_path, zones, directory_template)
