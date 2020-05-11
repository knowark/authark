from .entity import Entity

class Rule(Entity):
    def __init__(self, **attributes) -> None:
        super().__init__(**attributes)
        self.id = attributes.get('id', '')
        self.group = attributes.get('group', '')
        self.sequence = attributes.get('sequence', '')
        self.name = attributes.get('name', '')
        self.target = attributes.get('target', '')
        self.domain = attributes.get('domain', '')
