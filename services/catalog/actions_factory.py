from services.catalog.get_resources_info_action import GetResourceInfoAction


class ActionsFactory:
    @staticmethod
    def resolve(request_type):
        if request_type == 1:
            return GetResourceInfoAction()

        return None
