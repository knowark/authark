from inspect import signature
from authark.application.services import (
    HashService, MemoryHashService)


def test_hash_service() -> None:
    methods = HashService.__abstractmethods__  # type: ignore
    assert 'generate_hash' in methods
    assert 'verify_password' in methods


def test_memory_hash_service_implementation() -> None:
    assert issubclass(MemoryHashService, HashService)


def test_memory_hash_service_generate_hash() -> None:
    value = "SECRET_PASSWORD"

    hash_service = MemoryHashService()
    result = hash_service.generate_hash(value)

    assert isinstance(result, str)
    assert result == "HASHED: SECRET_PASSWORD"


def test_memory_hash_service_verify_password() -> None:
    hash_service = MemoryHashService()
    password = "SECRET_PASSWORD"
    hashed_password = "HASHED: SECRET_PASSWORD"

    result = hash_service.verify_password(password, hashed_password)
    assert result is True
    result = hash_service.verify_password("WRONG_PASSWORD", hashed_password)
    assert result is False
