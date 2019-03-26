class Grant:
    def __init__(self, **attributes) -> None:
        self.id = attributes.get('id', '')
        self.permission_id = attributes['permission_id']
        self.role_id = attributes['role_id']
