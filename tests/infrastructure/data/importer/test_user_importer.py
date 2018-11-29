from pytest import fixture
from authark.infrastructure.data.importer import UserImporter


@fixture
def user_importer(user_repository):

    user_importer = UserImporter(user_repository)
    return user_importer


def test_user_importer_instantiation(user_importer):
    assert user_importer is not None


def test_user_import(user_importer, import_users):
    result = user_importer.import_(import_users)
