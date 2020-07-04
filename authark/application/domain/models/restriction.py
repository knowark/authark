from .entity import Entity


class Restriction(Entity):
    def __init__(self, **attributes) -> None:
        super().__init__(**attributes)
        self.id = attributes.get('id', '')
        self.policy_id = attributes.get('policy_id', '')
        self.sequence = attributes.get('sequence', '')
        self.name = attributes.get('name', '')
        self.target = attributes.get('target', '')
        self.domain = attributes.get('domain', '')
