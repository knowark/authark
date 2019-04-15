from authark.application.repositories import Repository


def test_repository_methods() -> None:
    methods = Repository.__abstractmethods__  # type: ignore
    assert '__init__' in methods
    assert 'get' in methods
    assert 'add' in methods
    assert 'update' in methods
    assert 'search' in methods
    assert 'remove' in methods
