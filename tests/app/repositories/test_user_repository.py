from authark.app.repositories import UserRepository


def test_user_repository() -> None:
    methods = UserRepository.__abstractmethods__
    assert 'get' in methods
