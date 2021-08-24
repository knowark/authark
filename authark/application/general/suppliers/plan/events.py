

class Event:
    def __init__(self, **attributes) -> None:
        self.__dict__.update(attributes)


class UserRegistered(Event):
    """User Registered Event"""


class PasswordReset(Event):
    """Password Reset Event"""
