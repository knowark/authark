from pytest import fixture
from authark.application.domain.models.refresh import Refresh


@fixture
def refresh():
    return Refresh(
        value='xyz123'
    )


def test_refresh_instantiation(refresh):
    assert refresh is not None


def test_refresh_attributes(refresh):
    assert refresh.value == 'xyz123'
