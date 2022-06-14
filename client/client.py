import socket
from time import time
import struct
from zlib import crc32

from requests import ConnectTimeout

from infrastructure.catalog_messages_util import CatalogMessagesUtil
from infrastructure.catalog_messages_errors import CatalogMessageError
from services.transfer.file_service_actions import SendFileAction

from config import \
    CATALOG_MESSAGES_TYPES,\
    FILE_SERVICE_TIMEOUT,\
    FILE_TRANSFER_PORT,\
    RESPONSE_STATUSES,\
    CATALOG_SERVICE_PORT,\
    CATALOG_SERVICE_BUFFER_LENGTH,\
    DEFAULT_RESOURCE_PATH,\
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

    def get_file_from_remote_host(self, address, name):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            serializer = InjectionContainer["serializer"]
            self.inc_counter()

            msg = CatalogMessagesUtil.generate_file_request(
                self.__version,
                0,
                CATALOG_MESSAGES_TYPES.FILE_REQUEST.value,
                self.__group_id,
                serializer.serialze({'filename': name}))

            s.connect((address, FILE_TRANSFER_PORT))

            try:
                s.sendall(msg)
                s.settimeout(FILE_SERVICE_TIMEOUT)
                data = s.recv(8)

                _, _, status, _, to_read = \
                    CatalogMessagesUtil.parse_file_response_header(
                        data, self.__version, self.__group_id)
                with open(DEFAULT_RESOURCE_PATH + name, 'wb') as f:
                    while to_read >= 1024:
                        body = s.recv(1024)
                        f.write(body)
                        to_read -= 1024
                    body = s.recv(to_read)
                    f.write(body)
                s.close()
            except socket.timeout:
                print("Response not received")
                

    def send_file_to_requester(self, args):
        SendFileAction.execute()
        # accept
        # Rozkodowanie ramki z requestem i znalezienie nazwy pliku
        # W nowym wątku:
        #   Stworzyć ramkę z długością pliku
        #   send / sendall zawartość pliku


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

