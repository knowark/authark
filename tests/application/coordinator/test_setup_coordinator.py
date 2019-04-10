from authark.application.models import User
from authark.application.coordinators.setup_coordinator import SetupCoordinator


def test_setup_coordinator_creation(
        setup_coordinator: SetupCoordinator) -> None:
    assert hasattr(SetupCoordinator, 'setup_catalog')


def test_setup_coordinator_setup_catalog(
        setup_coordinator: SetupCoordinator) -> None:
    setup_coordinator.setup_catalog()
