import struct
from zlib import crc32
from infrastructure.catalog_messages_errors import \
    VersionNotSupported,\
    CrcCheckFailedError,\
    ExpiredRequestMessageError,\
    OtherGroupIdError,\
    MessageLengthInvalidError,\
    InvalidBodyError


class CatalogMessagesUtil:
    @staticmethod
    def __generate_msg(version, flags, type_code, group_id,
                       msg_id, body=None):

        rows = []
        rows.append(struct.pack(
                    '!BBH', (version << 4) + (flags & 0b1111),
                    type_code,
                    group_id))

        rows.append(struct.pack(
                    '!HH',
                    msg_id,
                    len(body) if body is not None else 0))

        if body is not None:
            rows.append(
                struct.pack(f'!{len(body)}s', body))

        rows.append(struct.pack('!L', crc32(b''.join(rows))))

        return b''.join(rows)

    @staticmethod
    def generate_request(version, flags, type, group_id,
                         msg_id, body=None):
        return CatalogMessagesUtil.__generate_msg(
            version, flags, type, group_id, msg_id, body)

    @staticmethod
    def generate_response(version, flags, code, group_id,
                          msg_id, body=None):
        return CatalogMessagesUtil.__generate_msg(
            version, flags, code, group_id, msg_id, body)

    @staticmethod
    def __parse_header(msg, checkVersion=None,
                       checkGroupId=None, checkMsgId=None):

        if len(msg) < 12:
            raise MessageLengthInvalidError()

        header = msg[0:8]
        crc = msg[-4:]

        version_flags, type_status, group_id = \
            struct.unpack('!BBH', header[0:4])

        msg_id, body_length = \
            struct.unpack('!HH', header[4:8])

        version = version_flags >> 4
        flags = version_flags & 0b1111

        # validate version
        if checkVersion is not None and version != checkVersion:
            raise VersionNotSupported(checkGroupId, msg_id)

        if checkGroupId is not None and group_id != group_id:
            raise OtherGroupIdError(checkGroupId, msg_id)

        if checkMsgId is not None and checkMsgId != msg_id:
            raise ExpiredRequestMessageError(group_id, msg_id)

        body = msg[8:-4]
        if body_length != len(body):
            raise InvalidBodyError(group_id, msg_id)

        if struct.unpack('!L', crc)[0] != crc32(header+body):
            raise CrcCheckFailedError(group_id, msg_id)

        return version, flags, type_status, group_id, msg_id, body_length

    @staticmethod
    def __parse_file_response_header(msg, checkVersion=None,
                                     checkGroupId=None, checkMsgId=None):

        if len(msg) < 12:
            raise MessageLengthInvalidError()

        header = msg[0:8]
        crc = msg[-4:]

        version_flags, response_code, group_id = \
            struct.unpack('!BBH', header[0:4])

        msg_id, body_length = \
            struct.unpack('!HH', header[4:8])

        version = version_flags >> 4
        flags = version_flags & 0b1111

        # validate version
        if checkVersion is not None and version != checkVersion:
            raise VersionNotSupported(checkGroupId, msg_id)

        if checkGroupId is not None and group_id != group_id:
            raise OtherGroupIdError(checkGroupId, msg_id)

        if checkMsgId is not None and checkMsgId != msg_id:
            raise ExpiredRequestMessageError(group_id, msg_id)

        body = msg[8:-4]
        if body_length != len(body):
            raise InvalidBodyError(group_id, msg_id)

        if struct.unpack('!L', crc)[0] != crc32(header+body):
            raise CrcCheckFailedError(group_id, msg_id)

        return version, flags, response_code, group_id, msg_id, body_length

    @staticmethod
    def parse_request_header(msg, checkVersion=None,
                             checkGroupId=None, checkMsgId=None):

        version, flags, type, group_id, msg_id, body_len = \
            CatalogMessagesUtil.__parse_header(
                msg, checkVersion, checkGroupId, checkMsgId)

        return version, flags, type, group_id, msg_id, body_len

    @staticmethod
    def parse_response_header(msg, checkVersion=None,
                              checkGroupId=None, checkMsgId=None):

        version, flags, type, group_id, msg_id, body_len = \
            CatalogMessagesUtil.__parse_header(
                msg, checkVersion, checkGroupId, checkMsgId)

        return version, flags, type, group_id, msg_id, body_len

    @staticmethod
    def parse_file_request_header(msg, checkVersion=None,
                                  checkGroupId=None, checkMsgId=None):

        version, flags, response_code, group_id, msg_id, body_len = \
            CatalogMessagesUtil.__parse_header(
                msg, checkVersion, checkGroupId, checkMsgId)

        return version, flags, response_code, group_id, msg_id, body_len

    @staticmethod
    def parse_file_response_header(msg, checkVersion=None,
                                   checkGroupId=None, checkMsgId=None):

        version, flags, type, group_id, msg_id, body_len = \
            CatalogMessagesUtil.__parse_file_response_header(
                msg, checkVersion, checkGroupId, checkMsgId)

        return version, flags, type, group_id, msg_id, body_len

    @staticmethod
    def parse_body(msg, checkVersion=None,
                   checkGroupId=None, checkMsgId=None):

        _, _, _, _, _, body_len = \
            CatalogMessagesUtil.__parse_header(
                msg, checkVersion, checkGroupId, checkMsgId)

        body = msg[8:-4]
        if body_len != len(body):
            raise InvalidBodyError()

        return body
    
    @staticmethod
    def parse_file_response_body(msg, checkVersion=None,
                                 checkGroupId=None, checkMsgId=None):

        _, _, _, _, _, body_len = \
            CatalogMessagesUtil.__parse_file_response_header(
                msg, checkVersion, checkGroupId, checkMsgId)

        body = msg[8:-4]
        if body_len != len(body):
            raise InvalidBodyError()

        return body
