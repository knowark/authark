from authark.application.models import Dominion


def test_dominion_creation():
    id_ = "af1209fade"
    name = "Data Server"
    url = "https://dataserver.nubark.com"

    dominion = Dominion(id=id_, name=name, url=url)

    assert dominion.id == id_
    assert dominion.name == name
    assert dominion.url == url
