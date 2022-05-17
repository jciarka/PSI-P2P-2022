from os import listdir
from os.path import isfile, join, getmtime

from config import InjectionContainer


class GetResourceInfoAction:
    def __init__(self) -> None:
        pass

    def execute(self, request, resource_path):
        resources = self.__list_resources(resource_path)

        serializer = InjectionContainer["serializer"]
        return serializer.serialze(resources)

    def __list_resources(self, resource_path):
        resources = [{"name": file,
                      "modified": getmtime(resource_path + '/' + file)}
                     for file in listdir(resource_path)
                     if isfile(join(resource_path, file))]

        return resources
