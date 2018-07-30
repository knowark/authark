from pytest import fixture
from passlib.hash import pbkdf2_sha256
from authark.application.services.hash_service import HashService
from authark.infrastructure.crypto.passlib_hash_service import (
    PasslibHashService)


def test_passlib_hash_service_implementation() -> None:
    assert issubclass(PasslibHashService, HashService)


def test_passlib_hash_service_generate_hash() -> None:
    passlib_hash_service = PasslibHashService()
    password = "SECRET_PASSWORD"
    hashed_password = passlib_hash_service.generate_hash(password)

    assert pbkdf2_sha256.verify(password, hashed_password)
