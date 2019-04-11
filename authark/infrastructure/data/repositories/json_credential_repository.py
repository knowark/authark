from authark.application.models.credential import Credential
from authark.application.utilities import ExpressionParser
from authark.application.repositories.credential_repository import (
    CredentialRepository)
from .json_repository import JsonRepository


class JsonCredentialRepository(
        JsonRepository[Credential], CredentialRepository):
    """Json Credential Repository"""

    def __init__(self, file_path: str, parser: ExpressionParser,
                 collection_name: str = 'credentials') -> None:
        super().__init__(file_path, parser, collection_name, Credential)
