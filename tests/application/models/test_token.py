from pytest import fixture
from authark.application.models.token import Token


@fixture
def token():
    return Token(
        value='xyz123'
    )


def test_token_instantiation(token):
    assert token is not None


def test_token_attributes(token):
    assert token.value == 'xyz123'


# def test_token_creation():
#     value = "xyz123"

#     token = Token(value=value)

#     assert token.value == value
#     assert isinstance(token.value, str)
