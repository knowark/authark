from authark.application.models import User
from authark.application.coordinators.setup_coordinator import SetupCoordinator


def test_setup_coordinator_creation(
        setup_coordinator: SetupCoordinator) -> None:
    assert hasattr(SetupCoordinator, 'import_users')


def test_setup_coordinator_import_users(
        setup_coordinator: SetupCoordinator) -> None:
    setup_coordinator.import_users(
        filepath='', source='erp.users', password_field='password')


def test_setup_coordinator_create_ranking_no_role(
        setup_coordinator: SetupCoordinator):
    user = User(username='Dummy', email='dummy@example.com')
    setup_coordinator._create_ranking(None, user)
    assert len(getattr(setup_coordinator.ranking_repository, 'items')) == 1
