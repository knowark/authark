import os
from abc import ABC, abstractmethod
from json import load, dump
from typing import Dict, List, Optional, Any
from authark.application.models.credential import Credential
from authark.application.utilities.type_definitions import QueryDomain
from authark.application.repositories.credential_repository import (
    CredentialRepository)
from authark.application.repositories.expression_parser import ExpressionParser


class JsonCredentialRepository(CredentialRepository):
    def __init__(self, file_path: str, parser: ExpressionParser) -> None:
        self.file_path = file_path
        self.parser = parser

    def get(self, id: str) -> Optional[Credential]:
        credential = None
        with open(self.file_path) as f:
            data = load(f)
            credentials = data.get('credentials') or {}
            credential = credentials.get(id)
            if credential:
                credential = Credential(**credential)
        return credential

    def add(self, credential: Credential) -> bool:
        data = {}  # type: Dict[str, Any]
        with open(self.file_path, 'r') as f:
            data = load(f)
        data['credentials'].update({credential.id: vars(credential)})
        with open(self.file_path, 'w') as f:
            dump(data, f)
        return True

    def search(self, domain: QueryDomain,
               limit=100, offset=0) -> List[Credential]:
        with open(self.file_path, 'r') as f:
            data = load(f)
            credentials_dict = data.get('credentials', {})

        credentials = []
        filter_function = self.parser.parse(domain)
        for credential_dict in list(credentials_dict.values()):
            credential = Credential(**credential_dict)
            if filter_function(credential):
                credentials.append(credential)

        if limit:
            credentials = credentials[:limit]
        if offset:
            credentials = credentials[offset:]
        return credentials

    def remove(self, credential: Credential) -> bool:
        with open(self.file_path, 'r') as f:
            data = load(f)
            credentials_dict = data.get('credentials')

        if credential.id not in credentials_dict:
            return False

        del credentials_dict[credential.id]

        with open(self.file_path, 'w') as f:
            dump(data, f)
        return True
