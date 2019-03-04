from authark.application.coordinators.setup_coordinator import SetupCoordinator


def test_setup_coordinator_creation(
        setup_coordinator: SetupCoordinator) -> None:
    assert hasattr(SetupCoordinator, 'import_users')


def test_setup_coordinator_import_users(
        setup_coordinator: SetupCoordinator) -> None:
    setup_coordinator.import_users(
        filepath='', source='erp.users', password_field='password')
