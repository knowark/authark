from authark.application.models.credential import Credential
from authark.application.repositories.credential_repository import (
    CredentialRepository)
from authark.infrastructure.data.json_repository import JsonRepository


class JsonCredentialRepository(
        JsonRepository[Credential], CredentialRepository):
    """Json Credential Repository"""
