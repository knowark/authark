from pytest import fixture, raises
from authark.application.domain.common import (
    User, AuthProvider, StandardAuthProvider,
    AuthenticationError, AuthorizationError)


def test_auth_provider_repository_methods():
    abstract_methods = AuthProvider.__abstractmethods__  # type: ignore

    assert 'setup' in abstract_methods
    assert 'user' in abstract_methods


@fixture
def auth_provider() -> StandardAuthProvider:
    # Given a memory auth_provider has been created
    auth_provider = StandardAuthProvider()
    auth_provider.setup(User(id='001', name="eecheverry"))
    return auth_provider


def test_standard_auth_provider(auth_provider):
    assert issubclass(StandardAuthProvider, AuthProvider)
    assert isinstance(auth_provider, AuthProvider)


def test_standard_auth_provider_verify(auth_provider):
    # Given a user
    user = User(id='U001', name="asb123", tid='T003')
    # When a user is given
    auth_provider.setup(user)
    # Then the user will be set
    assert auth_provider.user.name == 'asb123'
    assert auth_provider.user.tid == 'T003'
    assert auth_provider.reference == 'U001'


def test_standard_auth_get_user(auth_provider):
    # When the get_user method is called
    user = auth_provider.user
    # Then the current request user is returned
    assert user.name == "eecheverry"


def test_standard_auth_raises_if_user_not_set(auth_provider):
    # Given an auth provider without user
    auth_provider.setup(None)
    # When the user property is invoked
    # Then an AuthenticationError is raised
    with raises(AuthenticationError):
        user = auth_provider.user


@fixture
def user() -> User:
    return User()


def test_user_creation(user: User) -> None:
    assert isinstance(user, User)


def test_user_default_attributes(user: User) -> None:
    assert user.id == ""
    assert user.name == ""
    assert user.email == ""
    assert user.tid == ""
    assert user.tenant == ""
    assert user.organization == ""
    assert user.zone == ""
    assert user.roles == []


def test_user_attributes_from_dict() -> None:
    user_dict = {
        "id": "46ab9e22-639c-400b-b17d-e1a579f2a7bf",
        "name": "Juan Camilo Vivanco",
        "email": "jcvivanco@nubark.com",
        "tid": "c2a4f54c-83a0-4cb1-944e-81da646c091e",
        "tenant": "solo_por_servicio",
        "organization": "Solo Por Servicio",
        "zone": "central",
        "roles": ['user', 'admin']
    }

    user = User(**user_dict)

    for key, value in user_dict.items():
        assert getattr(user, key) == value


def test_standard_auth_provider_tenant_properties(auth_provider):
    # Given a user
    user = User(id='U001', name="asb123",
                tid='T003', tenant='solo_por_servicio',
                organization='Solo Por Servicio',
                zone='north')
    # When a user is given
    auth_provider.setup(user)
    # Then the user will be set
    assert auth_provider.user.id == 'U001'
    assert auth_provider.user.name == 'asb123'
    assert auth_provider.user.tid == 'T003'
    assert auth_provider.reference == 'U001'
    assert auth_provider.location == 'T003'
    assert auth_provider.zone == 'north'
