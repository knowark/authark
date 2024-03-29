from typing import Dict, Union
from modelark import Entity


Attributes = Dict[str, Union[int, str, float]]


class User(Entity):
    def __init__(self, **attributes):
        super().__init__(**attributes)
        self.email = attributes.get('email', '')
        self.username = attributes.get('username', '')
        self.name = attributes.get('name', '')
        self.picture = attributes.get('picture', '')
        self.active = attributes.get('active', True)
        self.attributes: Attributes = attributes.get(
            'attributes', {})
