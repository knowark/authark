from authark.application.models import User
from authark.application.coordinators import ImportCoordinator


async def test_import_coordinator_creation(import_coordinator) -> None:
    assert hasattr(ImportCoordinator, 'import_users')


async def test_import_coordinator_import_users(import_coordinator) -> None:
    await import_coordinator.import_users(
        filepath='', source='erp.users', password_field='password')


async def test_import_coordinator_create_ranking_no_role(import_coordinator):
    user = User(username='Dummy', email='dummy@example.com')
    await import_coordinator._create_ranking(None, user)
    assert len(getattr(import_coordinator.ranking_repository, 'data')[
               'default']) == 2
