from authark.application.models import Role


def test_role_creation() -> None:
    id_ = "1"
    name = "admin"
    dominion_id = "1"
    description = "System's Administrator"

    role = Role(id=id_, name=name, dominion_id=dominion_id,
                description=description)

    assert role.id == id_
    assert role.name == name
    assert role.dominion_id == dominion_id
    assert role.description == description
