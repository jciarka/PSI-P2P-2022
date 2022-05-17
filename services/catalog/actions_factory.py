from services.catalog.client_server_actions import GetResourceInfoAction


class ActionsFactory:
    @staticmethod
    def resolve(request_type):
        if request_type == 1:
            return GetResourceInfoAction()

        return None
