from os import listdir
from os.path import isfile, join, getmtime

from infrastructure.local_resources_util import LocalResourcesUtil
from config import InjectionContainer
from infrastructure.resource import Resource


class UpdateResourcesAction:
    def __init__(self) -> None:
        pass

    def execute(self, address, body, resources, resource_path):
        serializer = InjectionContainer["serializer"]
        items = serializer.deserialzie(body)

        resources.remove(address)
        for item in items:
            resource = Resource(item['name'])
            resource.append(address, item["modified"])
            resources.append(resource)

    def __list_resources(self, resource_path):
        resources = [{"name": file,
                      "modified": getmtime(resource_path + '/' + file)}
                     for file in listdir(resource_path)
                     if isfile(join(resource_path, file))]

        return resources


class GetResourceInfoAction:
    def __init__(self) -> None:
        pass

    def execute(self, address, body, resources, resource_path):
        resources = LocalResourcesUtil.get(resource_path)

        serializer = InjectionContainer["serializer"]
        return serializer.serialze(resources)


class GetRequestedFile:
    def __init__(self) -> None:
        pass

    def execute(self, address, body, resources, resource_path):
        serializer = InjectionContainer["serializer"]
        items = serializer.deserialzie(body)
        return items
