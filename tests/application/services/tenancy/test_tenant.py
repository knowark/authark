from pytest import fixture
from authark.application.services import Tenant


@fixture
def tenant() -> Tenant:
    return Tenant()


def test_tenant_creation(tenant: Tenant) -> None:
    assert isinstance(tenant, Tenant)


def test_user_default_attributes(tenant: Tenant) -> None:
    assert tenant.id == ""
    assert tenant.created_at > 0
    assert tenant.updated_at > 0
    assert tenant.name == ""


def test_user_attributes_from_dict() -> None:

    tenant_dict = {
        "id": "farbo007",
        "name": "hortofruticola_el_carino"
    }

    tenant = Tenant(**tenant_dict)

    for key, value in tenant_dict.items():
        assert getattr(tenant, key) == value

    assert tenant.created_at > 0
    assert tenant.updated_at > 0
