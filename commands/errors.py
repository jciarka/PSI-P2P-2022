class InvalidCommandError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class ShutDownSystemError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
