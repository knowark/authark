class Dominion:
    def __init__(self, **attributes) -> None:
        self.id = attributes['id']
        self.name = attributes['name']
        self.url = attributes.get('url', '')
