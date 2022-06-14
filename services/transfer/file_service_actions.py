# from os import listdir
# from os.path import isfile, join, getmtime
from config import InjectionContainer
# from infrastructure.local_resources_util import LocalResourcesUtil


class SendFileActionAction:
    def __init__(self, connection, address) -> None:
        self.__connection = connection,
        self.__address = address

    def execute(self):
        # serializer = InjectionContainer["serializer"]
        # data = serializer.deserialzie(body)

        # TODO: implement response for send file requirement

        pass
        # wywłanie pliku
