from authark.app.coordinators.auth_coordinator import AuthCoordinator


def test_auth_coordinator() -> None:
    auth_coordinator = AuthCoordinator()
    assert hasattr(auth_coordinator, 'authenticate')
