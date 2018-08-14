from json import dumps, loads
from pytest import fixture
from authark.application.models.user import User
from authark.application.repositories.user_repository import UserRepository
from authark.infrastructure.data.json_user_repository import JsonUserRepository


@fixture
def user_repository(tmpdir) -> JsonUserRepository:
    user_dict = {
        "valenep": vars(User('1', 'valenep', 'valenep@gmail.com', "PASS1")),
        "tebanep": vars(User('2', 'tebanep', 'tebanep@gmail.com', "PASS2")),
        "gabeche": vars(User('3', 'gabeche', 'gabeche@gmail.com', "PASS3"))
    }

    file_path = str(tmpdir.mkdir("authark").join('authark_data.json'))
    with open(file_path, 'w') as f:
        data = dumps({'users': user_dict})
        f.write(data)

    user_repository = JsonUserRepository(file_path=file_path)

    return user_repository


def test_json_user_repository_implementation() -> None:
    assert issubclass(JsonUserRepository, UserRepository)


def test_json_user_repository_get_user(
        user_repository: JsonUserRepository) -> None:

    user = user_repository.get("valenep")

    assert user and user.username == "valenep"
    assert user and user.email == "valenep@gmail.com"


def test_json_user_repository_save_user(
        user_repository: JsonUserRepository) -> None:

    user = User('', 'matiasve', 'matiasve@gmail.com', "PASS4")
    user_repository.save(user)

    file_path = user_repository.file_path
    with open(file_path) as f:
        data = loads(f.read())
        users_dict = data.get("users")

        user_dict = users_dict.get('matiasve')

        assert user_dict.get('username') == user.username
        assert user_dict.get('email') == user.email
        assert user_dict.get('password') == user.password


def test_json_user_repository_search_all(user_repository):
    users = user_repository.search([])

    assert len(users) == 3


def test_json_user_repository_search_limit(user_repository):
    users = user_repository.search([], limit=2)

    assert len(users) == 2


def test_json_user_repository_search_offset(user_repository):
    users = user_repository.search([], offset=2)

    assert len(users) == 1
