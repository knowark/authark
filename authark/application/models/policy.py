class Policy:
    def __init__(self, **attributes) -> None:
        self.id = attributes.get('id', '')
        self.type = attributes.get('type') or 'role'
        self.name = attributes.get('name', '')
        self.value = attributes['value']
