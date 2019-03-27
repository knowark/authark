from authark.application.models import Resource


def test_resource_creation() -> None:
    id_ = "001"
    name = "products"
    dominion_id = "001"

    resource = Resource(id=id_, name=name, dominion_id=dominion_id)

    assert resource.id == id_
    assert resource.name == name
    assert resource.dominion_id == dominion_id
