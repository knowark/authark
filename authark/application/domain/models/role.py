from modelark import Entity


class Role(Entity):
    def __init__(self, **attributes):
        super().__init__(**attributes)
        self.name = attributes['name']
        self.dominion_id = attributes.get('dominion_id', '')
        self.description = attributes.get('description', '')
