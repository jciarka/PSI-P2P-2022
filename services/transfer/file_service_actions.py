# from os import listdir
# from os.path import isfile, join, getmtime
import socket
import struct
from config import \
    VERSION,\
    FILE_SERVICE_ONE_READ_LEN,\
    RESOURCE_GROUP_ID,\
    DEFAULT_RESOURCE_PATH,\
    InjectionContainer,\
    FILE_TRANSFER_PORT,\
    RESPONSE_STATUSES,\
    FILE_SERVICE_REQUEST_HEADER_LEN

from infrastructure.catalog_messages_util import \
    CatalogMessagesUtil


from infrastructure.catalog_messages_errors import \
    StatusCodeException


class SendFileAction:
    def __init__(self, connection, address) -> None:
        self.__socket = connection
        self.__address = address

    def execute(self):
        try:
            body = b''
            header = self.__socket.recv(FILE_SERVICE_REQUEST_HEADER_LEN)

            _, _, group_id, msg_len = \
                CatalogMessagesUtil.parse_file_request_header(
                    header, VERSION, RESOURCE_GROUP_ID)

            while len(body) < msg_len:
                data = self.__socket.recv(FILE_SERVICE_ONE_READ_LEN)
                body += data

            serializer = InjectionContainer['serializer']
            file_name = serializer.deserialzie(body)['filename']

            with open(DEFAULT_RESOURCE_PATH + '/' + file_name, 'rb') as f:
                file_data = f.read()

            response = CatalogMessagesUtil.generate_file_response(
                    VERSION, 0, RESPONSE_STATUSES.SUCCESS.value,
                    group_id, file_data)

            self.__socket.sendall(response)
            self.__socket.close()

        except OSError as e:
            response = CatalogMessagesUtil.generate_file_response(
                VERSION, 0, RESPONSE_STATUSES.NOT_FOUND.value, group_id)

            self.__socket.sendto(response)
            return

        except StatusCodeException as ex:
            response = CatalogMessagesUtil.generate_file_response(
                VERSION, 0, ex.GetStatusCode().value,
                ex.get_group_id)

            self.__socket.sendall(response)
            return

        except (socket.timeout, Exception) as e:
            response = CatalogMessagesUtil.generate_file_response(
                VERSION, 0, RESPONSE_STATUSES.SERVER_ERROR.value, group_id)

            self.__socket.sendto(response)
            return
