

class Job:
    def __init__(self, **attributes) -> None:
        self.__dict__.update(attributes)
