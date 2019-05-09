from typing import Dict
from passlib.hash import pbkdf2_sha256
from ....application.services import HashService


class PasslibHashService(HashService):

    def __init__(self) -> None:
        pass

    def generate_hash(self, value: str) -> str:
        return pbkdf2_sha256.hash(value)

    def verify_password(self, password: str, hash: str) -> bool:
        return pbkdf2_sha256.verify(password, hash)
