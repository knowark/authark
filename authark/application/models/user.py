class User:
    def __init__(self, id: str, username: str,
                 email: str, password: str) -> None:
        self.id = id
        self.username = username
        self.email = email
        self.password = password
