import argparse
from infrastructure.resources import Resources
from infrastructure.resource import Resource
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
    results, _, _ = client.get_resources_info()

    for result in results:
        address = result[0]
        items = result[1]
        for item in items:
            resource = Resource(item['name'])
            resource.append(address, item["modified"])
            resources.append(resource)


def get_all_resources(client, path, resources: Resources):
    resources.clear()
    get_local_resources(path, resources)
    get_remote_resources(client, resources)


class Ls():
    def __init__(self, args) -> None:
        parser = Ls.__getParser()
        try:
            self.args = parser.parse_args(args)
        except SystemExit:
            raise InvalidCommandError()

    @staticmethod
    def __getParser():
        parser = argparse.ArgumentParser(
            "Command LS", description="lists resources")

        parser.add_argument("-l", "--local", action='store_true',
                            help='shows only local')
        parser.add_argument("-r", "--refresh", action='store_true',
                            help='forces refresh info from remote hosts')

        return parser

    @staticmethod
    def print_usage():
        return Ls.__getParser().print_help()

    def execute(self, client, resources=Resources(),
                resource_path=DEFAULT_RESOURCE_PATH):

        if self.args.refresh:
            resources.clear()
            get_local_resources(resource_path, resources)
            get_remote_resources(client, resources)

        if self.args.local:
            local = Resources()
            get_local_resources(resource_path, local)
            print(local)
        else:
            print(resources)
