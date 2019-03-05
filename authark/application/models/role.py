class Role:
    def __init__(self, **attributes) -> None:
        self.id = attributes.get('id', '')
        self.name = attributes['name']
        self.dominion_id = attributes.get('dominion_id', '')
        self.description = attributes.get('description', '')
