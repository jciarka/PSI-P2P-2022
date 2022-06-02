from config import CATALOG_MESSAGES_TYPES
from services.catalog.client_server_actions import \
    GetRequestedFile,\
    GetResourceInfoAction,\
    UpdateResourcesAction


class ActionsFactory:
    @staticmethod
    def resolve(request_type):
        if request_type == \
                CATALOG_MESSAGES_TYPES.BROADCAST_ALL_FILES.value:
            return UpdateResourcesAction()

        if request_type == \
                CATALOG_MESSAGES_TYPES.ALL_FILES_REQUEST.value:
            return GetResourceInfoAction()

        if request_type == \
                CATALOG_MESSAGES_TYPES.FILE_REQUEST.value:
            return GetRequestedFile()

        return None
