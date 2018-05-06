import pytest
from authark.application.models.error import AuthError


def test_auth_error_raises() -> None:
    with pytest.raises(AuthError):
        raise AuthError("Authentication Error!")
