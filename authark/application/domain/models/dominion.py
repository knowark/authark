from modelark import Entity


class Dominion(Entity):
    def __init__(self, **attributes):
        super().__init__(**attributes)
        self.name = attributes['name']
        self.url = attributes.get('url', '')
