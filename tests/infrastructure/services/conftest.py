from pytest import fixture
from authark.infrastructure.core import PyJWTTokenService


@fixture
def pyjwt_service():
    secret = 'ABCDE12345'
    algorithm = 'HS256'
    expiration = 1539715900
    payload = {'user': "Pepe",
               'email': "pepe@gmail.com",
               'exp': expiration}
    lifetime = 3600
    threshold = 60

    pyjwt_service = PyJWTTokenService(
        secret=secret, algorithm=algorithm,
        lifetime=lifetime, threshold=threshold)

    return pyjwt_service
