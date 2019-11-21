from .types import Attributes


class User:
    def __init__(self, **attributes) -> None:
        self.id = attributes.get('id', '')
        self.username = attributes['username']
        self.email = attributes['email']
        self.name = attributes.get('name', '')
        self.attributes: Attributes = attributes.get(
            'attributes', {})
