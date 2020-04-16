from .entity import Entity
from .types import Attributes


class User(Entity):
    def __init__(self, **attributes):
        super().__init__(**attributes)
        self.username = attributes['username']
        self.email = attributes['email']
        self.name = attributes.get('name', '')
        self.attributes: Attributes = attributes.get(
            'attributes', {})
