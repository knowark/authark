# from authark.application.models import User
# from authark.application.coordinators import ImportCoordinator


# def test_import_coordinator_creation(
#         import_coordinator: ImportCoordinator) -> None:
#     assert hasattr(ImportCoordinator, 'import_users')


# def test_import_coordinator_import_users(
#         import_coordinator: ImportCoordinator) -> None:
#     import_coordinator.import_users(
#         filepath='', source='erp.users', password_field='password')


# def test_import_coordinator_create_ranking_no_role(
#         import_coordinator: ImportCoordinator):
#     user = User(username='Dummy', email='dummy@example.com')
#     import_coordinator._create_ranking(None, user)
#     assert len(getattr(import_coordinator.ranking_repository, 'data')[
#                'default']) == 1
