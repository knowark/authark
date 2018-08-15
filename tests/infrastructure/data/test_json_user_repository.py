from json import dumps, loads
from pytest import fixture
from authark.application.models.user import User
from authark.application.repositories.user_repository import UserRepository
from authark.application.repositories.expression_parser import ExpressionParser
from authark.infrastructure.data.json_user_repository import JsonUserRepository


@fixture
def user_repository(tmpdir) -> JsonUserRepository:
    user_dict = {
        "1": vars(User('1', 'valenep', 'valenep@gmail.com', "PASS1")),
        "2": vars(User('2', 'tebanep', 'tebanep@gmail.com', "PASS2")),
        "3": vars(User('3', 'gabeche', 'gabeche@gmail.com', "PASS3"))
    }

    file_path = str(tmpdir.mkdir("authark").join('authark_data.json'))
    with open(file_path, 'w') as f:
        data = dumps({'users': user_dict})
        f.write(data)

    parser = ExpressionParser()
    user_repository = JsonUserRepository(file_path=file_path,
                                         parser=parser)

    return user_repository


def test_json_user_repository_implementation() -> None:
    assert issubclass(JsonUserRepository, UserRepository)


def test_json_user_repository_get_user(
        user_repository: JsonUserRepository) -> None:

    user = user_repository.get("1")

    assert user and user.username == "valenep"
    assert user and user.email == "valenep@gmail.com"


def test_json_user_repository_save_user(
        user_repository: JsonUserRepository) -> None:

    user = User('5', 'matiasve', 'matiasve@gmail.com', "PASS4")
    user_repository.save(user)

    file_path = user_repository.file_path
    with open(file_path) as f:
        data = loads(f.read())
        users_dict = data.get("users")

        user_dict = users_dict.get('5')

        assert user_dict.get('username') == user.username
        assert user_dict.get('email') == user.email
        assert user_dict.get('password') == user.password


def test_json_user_repository_search(user_repository):
    domain = [('username', '=', "gabeche")]

    users = user_repository.search(domain)

    assert len(users) == 1
    for user in users:
        assert user.id == '3'
        assert user.username == "gabeche"


def test_json_user_repository_search_all(user_repository):
    users = user_repository.search([])

    assert len(users) == 3


def test_json_user_repository_search_limit(user_repository):
    users = user_repository.search([], limit=2)

    assert len(users) == 2


def test_json_user_repository_search_offset(user_repository):
    users = user_repository.search([], offset=2)

    assert len(users) == 1


def test_json_user_repository_delete_user_true(user_repository):
    file_path = user_repository.file_path
    with open(file_path) as f:
        data = loads(f.read())
        users_dict = data.get("users")
        user_dict = users_dict.get('2')

    user = User(**user_dict)
    deleted = user_repository.delete(user)

    with open(file_path) as f:
        data = loads(f.read())
        users_dict = data.get("users")

    assert deleted is True
    assert len(users_dict) == 2
    assert "2" not in users_dict.keys()


def test_json_user_repository_delete_user_false(user_repository):
    file_path = user_repository.file_path
    user = User(**{'id': '6', 'username': 'MISSING',
                   'email': '', 'password': ''})
    deleted = user_repository.delete(user)

    with open(file_path) as f:
        data = loads(f.read())
        users_dict = data.get("users")

    assert deleted is False
    assert len(users_dict) == 3
