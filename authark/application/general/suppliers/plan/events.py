

class Event:
    def __init__(self, **attributes) -> None:
        self.__dict__.update(attributes)


class UserRegistered(Event):
    """User Registered Event"""
