from .entity import Entity


class Policy(Entity):
    def __init__(self, **attributes) -> None:
        super().__init__(**attributes)
        self.id = attributes.get('id', '')
        self.resource = attributes.get('resource', '')
        self.privilege = attributes.get('privilege', '')
        self.role_id = attributes.get('role_id', '')
        self.restriction = attributes.get('restriction', '')
