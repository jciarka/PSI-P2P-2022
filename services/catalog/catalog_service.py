import socket
from config import \
    VERSION,\
    RESOURCE_GROUP_ID,\
    CATALOG_SERVICE_PORT,\
    CATALOG_SERVICE_TIMEOUT,\
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

    def __init__(self, resources, path) -> None:
        self.cancelation_token = False

        self.__resources = resources
        self.__path = path

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

                    request_body = CatalogMessagesUtil.parse_body(
                        msg, VERSION, RESOURCE_GROUP_ID)

                except StatusCodeException as ex:
                    response = CatalogMessagesUtil.generate_response(
                        VERSION, 0, ex.GetStatusCode().value,
                        ex.get_group_id, ex.get_message_id)
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
                body = action.execute(
                    address[0], request_body,  self.__resources, self.__path)
                response = CatalogMessagesUtil.generate_response(
                    VERSION, 0, RESPONSE_STATUSES.SUCCESS.value,
                    group_id, msg_id, body)
                s.sendto(response, address)


if __name__ == "__main__":
    service = CatalogService()
    service.run()
