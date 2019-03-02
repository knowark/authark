from .types import Attributes


class User:
    def __init__(self, **attributes) -> None:
        self.id = attributes.get('id', '')
        self.external_source = attributes.get('external_source', '')
        self.external_id = attributes.get('external_id', '')
        self.username = attributes['username']
        self.email = attributes['email']
        self.name = attributes.get('name', '')
        self.gender = attributes.get('gender', '')
        self.attributes = attributes.get(
            'attributes', {})  # type: Attributes
