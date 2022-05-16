import socket
from time import time
import struct
from zlib import crc32

from client.errors import CrcCheckFailedError,\
    ExpiredRequestMessageError,\
    NotSuccessStatusError,\
    MessageLengthInvalidError,\
    InvalidBodyError

from config import \
    CATALOG_SERVICE_PORT,\
    VERSION,\
    CATALOG_SERVICE_BUFFER_LENGTH,\
    RESPONSE_STATUSES,\
    InjectionContainer


class Client:
    def __init__(self, delay_time_s, data_valid_time) -> None:
        self.counter = 0
        self.delay_time_s = delay_time_s
        self.data_valid_time = data_valid_time

    def get_resources_info(self):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:

            # sending request
            msg, msg_ident = self.__get_resources_info_prepare_message()
            s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            s.sendto(msg, ('255.255.255.255', CATALOG_SERVICE_PORT))

            # gathering responses
            gathered_info, errors_info = \
                self.__gather_responses_with_body(s, msg_ident)

            return gathered_info, errors_info

    def __get_resources_info_prepare_message(self):
        self.counter += 1
        rows = []
        rows.append(struct.pack('!BBh', (VERSION << 4), (1), self.counter))
        rows.append(struct.pack('!L', crc32(b''.join(rows))))

        return b''.join(rows), self.counter

    def __gather_responses_with_no_body(self, ready_socket, msg_ident):
        wait_unitl = time() + self.delay_time_s
        gathered_info = []
        errors_info = []

        while time() < wait_unitl:
            ready_socket.settimeout(wait_unitl - time())

            try:
                gathered_info.append(
                    self.__get_response_with_no_body(ready_socket, msg_ident))
            except CrcCheckFailedError as error:
                errors_info.append(
                    CrcCheckFailedError.__name__,
                    None, error.address)
            except ExpiredRequestMessageError as error:
                errors_info.append(
                    ExpiredRequestMessageError.__name__,
                    error.ident, error.address)
            except MessageLengthInvalidError as error:
                errors_info.append(
                    MessageLengthInvalidError.__name__,
                    error.status, error.address)
            except socket.timeout:
                break

        return gathered_info, errors_info

    def __get_response_with_no_body(self, ready_socket, request_ident):
        data_address = ready_socket.recvfrom(CATALOG_SERVICE_BUFFER_LENGTH)

        response = data_address[0]
        address = data_address[1]

        header = response[0:4]
        crc = response[-4:]

        _, status, response_ident = struct.unpack('!BBh', header[0:4])

        if request_ident != response_ident:
            raise ExpiredRequestMessageError(address, response_ident)

        if len(response) != 8:
            raise MessageLengthInvalidError(address)

        if struct.unpack('!L', crc)[0] != crc32(header):
            raise CrcCheckFailedError(address)

        return address[0], status

    def __gather_responses_with_body(self, ready_socket, msg_ident):
        wait_unitl = time() + self.delay_time_s
        gathered_info = []
        errors_info = []

        while time() < wait_unitl:
            ready_socket.settimeout(wait_unitl - time())

            try:
                gathered_info.append(
                    self.__get_response_with_body(ready_socket, msg_ident))
            except CrcCheckFailedError as error:
                errors_info.append(
                    CrcCheckFailedError.__name__,
                    None, error.address)
            except ExpiredRequestMessageError as error:
                errors_info.append(
                    ExpiredRequestMessageError.__name__,
                    error.ident, error.address)
            except NotSuccessStatusError as error:
                errors_info.append(
                    NotSuccessStatusError.__name__,
                    error.status, error.address)
            except MessageLengthInvalidError as error:
                errors_info.append(
                    MessageLengthInvalidError.__name__,
                    error.status, error.address)
            except socket.timeout:
                break

        return gathered_info, errors_info

    def __get_response_with_body(self, ready_socket, request_ident):
        data_address = ready_socket.recvfrom(CATALOG_SERVICE_BUFFER_LENGTH)

        response = data_address[0]
        address = data_address[1]

        header = response[0:8]
        crc = response[-4:]

        _, status, response_ident = struct.unpack('!BBh', header[0:4])
        body_length = struct.unpack('!L', header[4:8])[0]

        if status != RESPONSE_STATUSES.SUCCESS.value:
            raise NotSuccessStatusError(address, status)

        if request_ident != response_ident:
            raise ExpiredRequestMessageError(address, response_ident)

        body = response[8:-4]
        if body_length != len(body):
            raise MessageLengthInvalidError(address)

        if struct.unpack('!L', crc)[0] != crc32(header+body):
            raise CrcCheckFailedError(address)

        data = self.__process_response_body(
            struct.unpack(f'!{body_length}s', body)[0])

        if data is None:
            raise InvalidBodyError(address)

        return address[0], data

    def __process_response_body(self, body):
        serializer = InjectionContainer["serializer"]
        return serializer.deserialzie(body)



    # def __get_resources_info_parse_message(self, msg):
    #     content = msg[0:-4]
    #     crc = msg[-4:]

    #     version_undef, type, counter = struct.unpack('!BBh', content[0:4])
    #     version = version_undef >> 4

    #     if struct.unpack('!L', crc)[0] != crc32(content):
    #         print("error")

    #     return version, type, counter
