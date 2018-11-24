class Ranking:
    def __init__(self, **attributes) -> None:
        self.id = attributes.get('id', '')
        self.user_id = attributes['user_id']
        self.role_id = attributes['role_id']
