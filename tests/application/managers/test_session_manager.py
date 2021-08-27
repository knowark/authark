

def test_session_manager_creation(session_manager):
    assert hasattr(session_manager, 'set_user')


def test_session_manager_set_user(session_manager):
    entry = {'data': {'name': 'jplozano'}}
    session_manager.set_user(entry)
    assert session_manager.auth_provider.user.name == 'jplozano'


def test_session_manager_get_user(session_manager):
    entry = {'data': {'name': 'jplozano'}}
    session_manager.set_user(entry)
    assert session_manager.get_user()['name'] == 'jplozano'
