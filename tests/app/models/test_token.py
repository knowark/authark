from authark.app.models.token import Token


def test_token_creation() -> None:
    value = "xyz123"

    token = Token(value=value)

    assert token.value == value
    assert isinstance(token.value, str)
