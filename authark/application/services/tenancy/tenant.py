import time


class Tenant:
    def __init__(self, **attributes):
        self.id = attributes.get('id', '')
        self.created_at = int(time.time())
        self.updated_at = int(time.time())
        self.name = attributes.get('name', '')
        self.email = attributes.get('email', '')
        self.active = attributes.get('active', True)
