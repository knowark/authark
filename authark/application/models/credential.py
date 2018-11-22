class Credential:
    def __init__(self, id: str, user_id: str, value: str,
                 type: str = 'password', client: str = 'ALL') -> None:
        self.id = id
        self.user_id = user_id
        self.type = type
        self.client = client
        self.value = value
