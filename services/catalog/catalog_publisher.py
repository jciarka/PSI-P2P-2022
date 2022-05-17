import socket
from time import sleep
from infrastructure.local_resources_util import LocalResourcesUtil
from config import \
    InjectionContainer,\
    CATALOG_SERVICE_PORT,\
    CATALOG_PUBLISHER_AWAKE_PERIOD,\
    CATALOG_PUBLISHER_SEND_PERIOD,\
    DEFAULT_RESOURCE_PATH,\
    RESOURCE_GROUP_ID,\
    CATALOG_MESSAGES_TYPES

from infrastructure.catalog_messages_util import CatalogMessagesUtil


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
                 version,
                 resource_path=DEFAULT_RESOURCE_PATH,
                 group_id=RESOURCE_GROUP_ID,
                 awake_period=CATALOG_PUBLISHER_AWAKE_PERIOD,
                 send_period=CATALOG_PUBLISHER_SEND_PERIOD,
                 ) -> None:

        self.cancelation_token = False
        self.__version = version
        self.__resource_path = resource_path
        self.__awake_period = awake_period
        self.__send_period = send_period
        self.__serialzier = InjectionContainer["serializer"]
        self.__group_id = group_id
        self.__wait = 0

    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:

            s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            while not self.cancelation_token:

                if not self.__process_should_send_now_or_delay():
                    continue

                resources = LocalResourcesUtil.get(self.__resource_path)
                body = self.__serialzier.serialze(resources)
                msg = CatalogMessagesUtil.generate_request(
                    self.__version,
                    0,
                    CATALOG_MESSAGES_TYPES.BROADCAST_ALL_FILES.value,
                    self.__group_id,
                    0,
                    body
                )
                s.sendto(msg, ('255.255.255.255', CATALOG_SERVICE_PORT))

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
