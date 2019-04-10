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


# def test_user_attributes_from_dict() -> None:

#     user_dict = {
#         "id": "XYZ123",
#         "name": "Julian David Martos",
#         "email": "jdmartos@nubark.com",
#         "external_id": "5432",
#         "external_source": "erp_system",
#         "attributes": {
#             "employee_id": "2349",
#             "partner_id": "7689"
#         }
#     }

#     user = User(**user_dict)

#     for key, value in user_dict.items():
#         assert getattr(user, key) == value
