from typing import Dict, Union
from modelark import Entity


Attributes = Dict[str, Union[int, str, float]]


class User(Entity):
    def __init__(self, **attributes):
        super().__init__(**attributes)
        self.username = attributes['username']
        self.email = attributes['email']
        self.name = attributes.get('name', '')
        self.active = attributes.get('active', True)
        self.attributes: Attributes = attributes.get(
            'attributes', {})
