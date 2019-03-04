class Credential:
    def __init__(self, **attributes) -> None:
        self.id = attributes.get('id', '')
        self.user_id = attributes.get('user_id', '')
        self.type = attributes.get('type', 'password')
        self.client = attributes.get('client', 'ALL')
        self.value = attributes['value']
