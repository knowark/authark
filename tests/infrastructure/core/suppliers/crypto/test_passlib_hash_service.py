from authark.infrastructure.core import PasslibHashService


def test_passlib_hash_service_instantiation(hash_service):
    assert isinstance(hash_service, PasslibHashService)


def test_passlib_hash_service_generate_hash(hash_service):
    result = hash_service.generate_hash('MY_SECRET_PASSWORD')
    assert '$pbkdf2-sha256' in result


def test_passlib_hash_service_verify_password(hash_service):
    result = hash_service.verify_password(
        'MY_SECRET_PASSWORD', (
            '$pbkdf2-sha256$29000$ICTkXOvdOyfknHPOGSOk9A$7zQceZ.'
            'zvA2qJINoz2qaRwabobQlXVMb0kZza/Ry3rM')
    )
    assert result is True
