from time import time
from tabulate import tabulate
from client.resource import Resource


class Resources:

    @property
    def timestamp(self) -> float:
        return self.__timestamp

    @property
    def resources(self) -> dict:
        return self.__resources

    def __init__(self, resources=[]) -> None:
        self.__timestamp = time()
        self.__resources = resources

    def append(self, resource: Resource):
        if resource.name not in (r.name for r in self.__resources):
            self.__resources.append(resource)
        else:
            existing = [r for r in self.__resources
                        if r.name == resource.name][0]

            for address, timestamp in resource.addresses_with_timestamp:
                existing.append(address, timestamp)

    def __str__(self) -> str:
        data = [r.get_display_data() for r in self.__resources]
        headers = ['prefered', 'has local', 'name', 'timestamp']
        return tabulate(data, headers=headers)

    def clear(self):
        self.__init__()
