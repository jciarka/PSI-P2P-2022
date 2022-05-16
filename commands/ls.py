import argparse
from client.resources import Resources
from client.resource import Resource
from os import listdir
from os.path import isfile, join, getmtime
from config import DEFAULT_RESOURCE_PATH, LOCAL_RESOURCE_ADDRESS
from commands.errors import InvalidCommandError


def get_local_resources(resource_path, resources: Resources):
    items = [{"name": file,
              "modified": getmtime(resource_path + '/' + file)}
             for file in listdir(resource_path)
             if isfile(join(resource_path, file))]

    address = LOCAL_RESOURCE_ADDRESS
    for item in items:
        resource = Resource(item['name'])
        resource.append(address, item["modified"])
        resources.append(resource)


def get_remote_resources(client, resources: Resources):
    results, _ = client.get_resources_info()

    for result in results:
        address = result[0]
        items = result[1]
        for item in items:
            resource = Resource(item['name'])
            resource.append(address, item["modified"])
            resources.append(resource)


class Ls():
    def __init__(self, args) -> None:
        parser = self.__getParser()
        try:
            self.args = parser.parse_args(args)
        except SystemExit:
            raise InvalidCommandError()

    def __getParser(self):
        parser = argparse.ArgumentParser(
            "Command ls")

        parser.add_argument("-l", "--local", action='store_true')
        return parser

    def execute(self, client, resources=Resources(),
                resource_path=DEFAULT_RESOURCE_PATH):

        resources.clear()

        get_local_resources(resource_path, resources)
        if not self.args.local:
            get_remote_resources(client, resources)

        print(resources)
        return resources
