from typing import Literal
from modelark import Entity


class Credential(Entity):
    def __init__(self, **attributes):
        super().__init__(**attributes)
        self.user_id = attributes.get('user_id', '')
        self.type: Literal[
            'password', 'refresh_token'] = attributes.get('type', 'password')
        self.client = attributes.get('client', 'ALL')
        self.value = attributes['value']
