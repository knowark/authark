from authark.app.repositories.user_repository import UserRepository


def test_user_repository() -> None:
    methods = UserRepository.__abstractmethods__
    assert 'get' in methods
    assert 'save' in methods
