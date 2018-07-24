from inspect import signature
from authark.application.services.hash_service import (
    HashService, MemoryHashService)


def test_hash_service() -> None:
    methods = HashService.__abstractmethods__
    assert 'generate_hash' in methods


def test_memory_hash_service_implementation() -> None:
    assert issubclass(MemoryHashService, HashService)


def test_memory_hash_service_generate_hash_with_payload() -> None:
    value = "SECRET_PASSWORD"

    hash_service = MemoryHashService()
    result = hash_service.generate_hash(value)

    assert isinstance(result, str)
    assert result == "HASHED: SECRET_PASSWORD"
