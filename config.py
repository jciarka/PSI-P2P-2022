from enum import Enum
from infrastructure.json_serializer import JsonSerializer

VERSION = 5
DEFAULT_RESOURCE_PATH = '/home/jakub/.PSI_P2P'
CATALOG_SERVICE_PORT = 30001
CATALOG_SERVICE_TIMEOUT = 5
CATALOG_SERVICE_BUFFER_LENGTH = 65535

TRANSFER_TRANSFER_PORT = 30002
LOCAL_RESOURCE_ADDRESS = '127.0.0.1'


class RESPONSE_STATUSES(Enum):
    SUCCESS = 0
    BAD_REQUEST = 100
    REQUEST_DAMMAGED = 101
    NOT_FOUND = 104


# register injection
InjectionContainer = {
    "serializer": JsonSerializer()
}
