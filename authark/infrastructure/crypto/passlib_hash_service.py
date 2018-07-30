from typing import Dict
from passlib.hash import pbkdf2_sha256
from authark.application.services.hash_service import HashService


class PasslibHashService(HashService):

    def __init__(self) -> None:
        pass

    def generate_hash(self, value: str) -> str:
        return pbkdf2_sha256.hash(value)
