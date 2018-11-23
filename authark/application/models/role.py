class Role:
    def __init__(self, **attributes) -> None:
        self.id = attributes['id']
        self.name = attributes['name']
        self.dominion_id = attributes['dominion_id']
        self.description = attributes.get('description', '')
