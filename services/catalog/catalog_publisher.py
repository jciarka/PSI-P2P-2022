import socket
import struct
from zlib import crc32
from time import sleep
from infrastructure.local_resources_util import LocalResourcesUtil
from config import \
    VERSION,\
    InjectionContainer,\
    CATALOG_SERVICE_PORT,\
    CATALOG_PUBLISHER_AWAKE_PERIOD,\
    CATALOG_PUBLISHER_SEND_PERIOD,\
    DEFAULT_RESOURCE_PATH,\
    CATALOG_MESSAGES_TYPES


class CatalogPublisher:
    @property
    def cancelation_token(self):
        return self.__cancelation_token

    @cancelation_token.setter
    def cancelation_token(self, value):
        self.__cancelation_token = value

    @property
    def resource_path(self):
        return self.__resource_path

    def __init__(self,
                 resource_path=DEFAULT_RESOURCE_PATH,
                 awake_period=CATALOG_PUBLISHER_AWAKE_PERIOD,
                 send_period=CATALOG_PUBLISHER_SEND_PERIOD) -> None:

        self.cancelation_token = False
        self.__resource_path = resource_path
        self.__awake_period = awake_period
        self.__send_period = send_period
        self.__serialzier = InjectionContainer["serializer"]
        self.__wait = 0

    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:

            s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            while not self.cancelation_token:

                if not self.__process_should_send_now_or_delay():
                    continue

                resources = LocalResourcesUtil.get(self.__resource_path)
                body = self.__serialzier.serialze(resources)
                msg = self.__generate_message(body)
                s.sendto(msg, ('255.255.255.255', CATALOG_SERVICE_PORT))

    def __generate_message(self, body):
        rows = []
        rows.append(struct.pack('!BBH',
                    (VERSION << 4) + (1 << 3),
                    CATALOG_MESSAGES_TYPES.BROADCAST_ALL_FILES.value,
                    len(body)))
        rows.append(struct.pack(f'!{len(body)}s', body))
        rows.append(struct.pack('!L', crc32(b''.join(rows))))
        return b''.join(rows)

    def __process_should_send_now_or_delay(self):
        if self.__wait > 0:
            sleep(self.__awake_period)
            self.__wait -= self.__awake_period
            return False

        self.__wait = self.__send_period
        return True


if __name__ == "__main__":
    dispacher = CatalogPublisher()
    dispacher.run()
