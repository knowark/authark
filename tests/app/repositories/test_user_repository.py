from inspect import signature
from authark.app.repositories.user_repository import UserRepository


def test_user_repository_methods() -> None:
    methods = UserRepository.__abstractmethods__
    assert 'get' in methods
    assert 'save_' in methods

    sig = signature(UserRepository.save)
    assert sig.parameters.get('user')
