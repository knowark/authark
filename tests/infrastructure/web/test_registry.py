from pytest import fixture
from authark.application.coordinators.auth_coordinator import AuthCoordinator
from authark.infrastructure.web.registry import Registry


def test_registry_type() -> None:
    assert issubclass(Registry, dict)


def test_registry_initialization() -> None:
    registry = Registry()

    assert isinstance(registry['auth_coordinator'], AuthCoordinator)
