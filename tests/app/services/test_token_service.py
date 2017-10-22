from inspect import signature
from authark.app.services.token_service import TokenService


def test_token_service() -> None:
    methods = TokenService.__abstractmethods__
    assert 'generate_token' in methods

    sig = signature(TokenService.generate_token)
    assert sig.parameters.get('payload')
