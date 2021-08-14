from authark.application.domain.models import User
from authark.application.domain.services import (
    IdentityService, MemoryIdentityService)


def test_identity_service_methods() -> None:
    methods = IdentityService.__abstractmethods__  # type: ignore
    assert 'identify' in methods


def test_memory_identity_service_instantiation() -> None:
    identity_service = MemoryIdentityService()

    assert isinstance(identity_service, IdentityService)


async def test_memory_identity_service_identify() -> None:
    user = User(email="mock@users.net")
    identity_service = MemoryIdentityService(user)
    user = await identity_service.identify(
        'google', 'secret1234')
    assert user.email == 'mock@users.net'
