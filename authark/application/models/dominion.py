class Dominion:
    def __init__(self, **attributes) -> None:
        self.id = attributes.get('id', '')
        self.name = attributes['name']
        self.url = attributes.get('url', '')
