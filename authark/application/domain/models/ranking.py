from .entity import Entity


class Ranking(Entity):
    def __init__(self, **attributes):
        super().__init__(**attributes)
        self.user_id = attributes.get('user_id', '')
        self.role_id = attributes.get('role_id', '')
