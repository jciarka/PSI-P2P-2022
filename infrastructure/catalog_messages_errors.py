from config import RESPONSE_STATUSES


class CatalogMessageError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class StatusCodeException(CatalogMessageError):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

    def GetStatusCode(self):
        raise NotImplementedError()


class VersionNotSupported(StatusCodeException):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

    def GetStatusCode(self):
        raise RESPONSE_STATUSES.VERSION_NOT_SUPPORTED


class CrcCheckFailedError(StatusCodeException):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

    def GetStatusCode(self):
        raise RESPONSE_STATUSES.REQUEST_DAMMAGED


class MessageLengthInvalidError(StatusCodeException):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

    def GetStatusCode(self):
        raise RESPONSE_STATUSES.REQUEST_DAMMAGED


class ExpiredRequestMessageError(Exception):
    def __init__(self, ident, *args: object) -> None:
        self.ident = ident
        super().__init__(*args)


class OtherGroupIdError(CatalogMessageError):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class InvalidBodyError(StatusCodeException):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

    def GetStatusCode(self):
        raise RESPONSE_STATUSES.REQUEST_DAMMAGED
