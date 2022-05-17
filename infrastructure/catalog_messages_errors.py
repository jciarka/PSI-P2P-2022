from config import RESPONSE_STATUSES


class CatalogMessageError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class StatusCodeException(CatalogMessageError):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

    def get_status_code(self):
        raise NotImplementedError()

    def get_message_id(self):
        raise NotImplementedError()

    def get_group_id(self):
        raise NotImplementedError()


class VersionNotSupported(StatusCodeException):
    def __init__(self, group_id, msg_id, *args: object) -> None:
        super().__init__(*args)
        self.message_id = msg_id
        self.group_id = group_id

    def get_status_code(self):
        return RESPONSE_STATUSES.VERSION_NOT_SUPPORTED

    def get_message_id(self):
        return self.message_id

    def get_group_id(self):
        return self.group_id


class CrcCheckFailedError(StatusCodeException):
    def __init__(self, group_id, msg_id, *args: object) -> None:
        super().__init__(*args)
        self.message_id = msg_id
        self.group_id = group_id

    def get_status_code(self):
        return RESPONSE_STATUSES.REQUEST_DAMMAGED

    def get_message_id(self):
        return self.message_id

    def get_group_id(self):
        return self.group_id


class MessageLengthInvalidError(CatalogMessageError):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

    def get_status_code(self):
        return RESPONSE_STATUSES.REQUEST_DAMMAGED

    def get_message_id(self):
        return 0

    def get_group_id(self):
        return 0


class ExpiredRequestMessageError(Exception):
    def __init__(self, group_id, msg_id, *args: object) -> None:
        super().__init__(*args)
        self.message_id = msg_id
        self.group_id = group_id

    def get_message_id(self):
        return self.message_id

    def get_group_id(self):
        return self.group_id


class OtherGroupIdError(CatalogMessageError):
    def __init__(self, group_id, msg_id, *args: object) -> None:
        super().__init__(*args)
        self.message_id = msg_id
        self.group_id = group_id

    def get_message_id(self):
        return self.message_id

    def get_group_id(self):
        return self.group_id


class InvalidBodyError(StatusCodeException):
    def __init__(self, group_id, msg_id, *args: object) -> None:
        super().__init__(*args)
        self.message_id = msg_id
        self.group_id = group_id

    def get_status_code(self):
        return RESPONSE_STATUSES.REQUEST_DAMMAGED

    def get_message_id(self):
        return self.message_id

    def get_group_id(self):
        return self.group_id
