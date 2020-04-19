# from pytest import fixture
# from passlib.hash import pbkdf2_sha256
# from authark.application.services import HashService
# from authark.infrastructure.core import PasslibHashService


# def test_passlib_hash_service_implementation() -> None:
#     assert issubclass(PasslibHashService, HashService)


# def test_passlib_hash_service_generate_hash() -> None:
#     passlib_hash_service = PasslibHashService()
#     password = "SECRET_PASSWORD"
#     hashed_password = passlib_hash_service.generate_hash(password)

#     assert pbkdf2_sha256.verify(password, hashed_password)


# def test_passlib_hash_service_verify_password() -> None:
#     hash_service = PasslibHashService()
#     password = "SECRET_PASSWORD"
#     hashed_password = pbkdf2_sha256.hash(password)

#     result = hash_service.verify_password(password, hashed_password)
#     assert result is True
#     result = hash_service.verify_password("WRONG_PASSWORD", hashed_password)
#     assert result is False
