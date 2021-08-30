from authark.application.domain.models import User
from authark.application.operation.managers import ImportManager


async def test_import_manager_creation(import_manager) -> None:
    assert hasattr(ImportManager, 'import_users')


async def test_import_manager_import_users(import_manager) -> None:
    await import_manager.import_users(
        filepath='', source='erp.users', password_field='password')


async def test_import_manager_create_ranking_no_role(import_manager):
    user = User(username='Dummy', email='dummy@example.com')
    await import_manager._create_ranking(None, user)
    assert len(getattr(import_manager.ranking_repository, 'data')[
               'default']) == 2
