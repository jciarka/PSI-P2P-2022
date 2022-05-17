import socket
from time import time
import struct
from zlib import crc32

from infrastructure.catalog_messages_util import CatalogMessagesUtil
from infrastructure.catalog_messages_errors import CatalogMessageError

from config import \
    CATALOG_MESSAGES_TYPES,\
    RESPONSE_STATUSES,\
    CATALOG_SERVICE_PORT,\
    CATALOG_SERVICE_BUFFER_LENGTH,\
    InjectionContainer


class Client:
    def __init__(self, delay_time_s, version, group_id) -> None:
        self.__counter = 0
        self.__delay_time_s = delay_time_s
        self.__version = version
        self.__group_id = group_id

    def inc_counter(self):
        self.__counter += 1

    def get_resources_info(self):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            self.inc_counter()
            msg_ident = self.__counter
            serializer = InjectionContainer["serializer"]

            msg = CatalogMessagesUtil.generate_request(
                self.__version,
                0,
                CATALOG_MESSAGES_TYPES.ALL_FILES_REQUEST.value,
                self.__group_id,
                self.__counter)

            s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            s.sendto(msg, ('255.255.255.255', CATALOG_SERVICE_PORT))

            # gathering responses
            success_info, send_errors, recieve_errors = \
                self.__gather_responses_with_body(s, msg_ident, serializer)

            return success_info, send_errors, recieve_errors

    def __gather_responses_with_body(self, ready_socket, msg_ident, serializer):
        wait_unitl = time() + self.__delay_time_s
        success_info = []
        send_errors = []
        recieve_errors = []

        while time() < wait_unitl:
            ready_socket.settimeout(wait_unitl - time())

            try:
                data, address = ready_socket.recvfrom(
                    CATALOG_SERVICE_BUFFER_LENGTH)

                _, _, status, _, _, _ = \
                    CatalogMessagesUtil.parse_response_header(
                        data, self.__version, self.__group_id, msg_ident)

                if status != RESPONSE_STATUSES.SUCCESS:
                    send_errors.append((address, status))

                body = CatalogMessagesUtil.parse_body(
                    data, self.__version, self.__group_id, msg_ident)

                success_info.append((address, serializer.deserialzie(body)))

            except CatalogMessageError as error:
                recieve_errors.append((address, type(error).__name__))
            except socket.timeout:
                break

        return success_info, send_errors, recieve_errors
