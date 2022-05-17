import socket
import struct
from zlib import crc32
from config import \
    VERSION,\
    RESOURCE_GROUP_ID,\
    CATALOG_SERVICE_PORT,\
    CATALOG_SERVICE_TIMEOUT,\
    DEFAULT_RESOURCE_PATH,\
    CATALOG_SERVICE_BUFFER_LENGTH,\
    RESPONSE_STATUSES

from services.catalog.actions_factory import ActionsFactory
from infrastructure.catalog_messages_util import CatalogMessagesUtil
from infrastructure.catalog_messages_errors import \
    StatusCodeException, CatalogMessageError


class CatalogService:
    @property
    def cancelation_token(self):
        return self.__cancelation_token

    @cancelation_token.setter
    def cancelation_token(self, value):
        self.__cancelation_token = value

    @property
    def resource_path(self):
        return self.__resource_path

    def __init__(self, resource_path=None) -> None:
        self.cancelation_token = False

        if not resource_path:
            self.__resource_path = DEFAULT_RESOURCE_PATH
        else:
            self.__resource_path = resource_path

    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.bind(('0.0.0.0', CATALOG_SERVICE_PORT))
            s.settimeout(CATALOG_SERVICE_TIMEOUT)

            while not self.cancelation_token:
                try:
                    msg, address = s.recvfrom(CATALOG_SERVICE_BUFFER_LENGTH)
                except socket.timeout:
                    continue

                try:
                    _, _, type, group_id, msg_id, _ = \
                        CatalogMessagesUtil.parse_response_header(
                            msg, VERSION, RESOURCE_GROUP_ID)

                except StatusCodeException as ex:
                    response = CatalogMessagesUtil.generate_response(
                        VERSION, 0, ex.GetStatusCode().value, group_id, msg_id)
                    s.sendto(response, address)
                    continue

                except CatalogMessageError:
                    # other problems that should not be handled
                    # like expired message
                    continue

                except Exception:
                    response = CatalogMessagesUtil.generate_response(
                        VERSION, 0, RESPONSE_STATUSES.SERVER_ERROR.value,
                        group_id, msg_id)
                    s.sendto(response, address)
                    continue

                # execute action
                action = ActionsFactory.resolve(type)
                body = action.execute(msg, resource_path=self.resource_path)
                response = CatalogMessagesUtil.generate_response(
                    VERSION, 0, RESPONSE_STATUSES.SUCCESS.value,
                    group_id, msg_id, body)
                s.sendto(response, address)

    def __validate_request(self, msg):
        version_flags, type, request_ident = \
            struct.unpack('!BBh', msg[0:4])

        # validate version
        if (version_flags >> 4) != VERSION:
            return False, RESPONSE_STATUSES.REQUEST_DAMMAGED

        # validate crc
        crc = msg[-4:]
        if struct.unpack('!L', crc)[0] != crc32(msg[0:-4]):
            return (False, RESPONSE_STATUSES.REQUEST_DAMMAGED)

        # resolve action class
        action = ActionsFactory.resolve(type)
        if action is None:
            return (False, RESPONSE_STATUSES.BAD_REQUEST)

        return True, action

    def __generate_error_response(self, request_ident, status_code):
        rows = []
        rows.append(struct.pack('!BBh', (VERSION << 4),
                    status_code.value, request_ident))

        rows.append(struct.pack('!L', crc32(b''.join(rows))))
        return b''.join(rows)

    def __generate_success_response(self, request_ident, body):
        rows = []
        rows.append(struct.pack('!BBh', (VERSION << 4),
                    RESPONSE_STATUSES.SUCCESS.value, request_ident))
        rows.append(struct.pack('!L', len(body)))
        rows.append(struct.pack(f'!{len(body)}s', body))
        rows.append(struct.pack('!L', crc32(b''.join(rows))))
        return b''.join(rows)


if __name__ == "__main__":
    service = CatalogService()
    service.run()
