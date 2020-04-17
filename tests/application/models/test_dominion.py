from pytest import fixture
from authark.application.models import Dominion


@fixture
def dominion():
    return Dominion(
        id='af1209fade',
        name='Data Server',
        url='https://dataserver.nubark.com'
    )


def test_dominion_instation(dominion):
    assert dominion is not None


def test_dominion_attributes(dominion):
    assert dominion.name == 'Data Server'
    assert dominion.url == 'https://dataserver.nubark.com'


# def test_dominion_creation():
#     id_ = "af1209fade"
#     name = "Data Server"
#     url = "https://dataserver.nubark.com"

#     dominion = Dominion(id=id_, name=name, url=url)

#     assert dominion.id == id_
#     assert dominion.name == name
#     assert dominion.url == url
