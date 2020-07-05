from .entity import Entity


class Policy(Entity):
    def __init__(self, **attributes) -> None:
        super().__init__(**attributes)
        self.id = attributes.get('id', '')
        self.role_id = attributes.get('role_id', '')
        self.resource = attributes.get('resource', '')
        self.active = attributes.get('active', False)
        self.privilege = attributes.get('privilege', '')
