class CrcCheckFailedError(Exception):
    def __init__(self, address, *args: object) -> None:
        self.address = address
        super().__init__(*args)


class MessageLengthInvalidError(Exception):
    def __init__(self, address, *args: object) -> None:
        self.address = address
        super().__init__(*args)


class ExpiredRequestMessageError(Exception):
    def __init__(self, address, ident, *args: object) -> None:
        self.address = address
        self.ident = ident
        super().__init__(*args)


class NotSuccessStatusError(Exception):
    def __init__(self, address, status, *args: object) -> None:
        self.address = address
        self.status = status
        super().__init__(*args)


class InvalidBodyError(Exception):
    def __init__(self, address, *args: object) -> None:
        self.address = address
        super().__init__(*args)
