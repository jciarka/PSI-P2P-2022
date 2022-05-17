from time import time
from tabulate import tabulate
from infrastructure.resource import Resource
from infrastructure.synchronized_decorator import synchronized
from threading import Lock


class Resources:
    @synchronized
    @property
    def timestamp(self) -> float:
        return self.__timestamp

    @synchronized
    @property
    def resources(self) -> dict:
        return self.__resources

    def __init__(self, resources=[]) -> None:
        self.lock = Lock()
        self.__timestamp = time()
        self.__resources = resources

    @synchronized
    def append(self, resource: Resource):
        if resource.name not in (r.name for r in self.__resources):
            self.__resources.append(resource)
        else:
            existing = [r for r in self.__resources
                        if r.name == resource.name][0]

            for address, timestamp in resource.addresses_with_timestamp:
                existing.append(address, timestamp)

    def __str__(self) -> str:
        self.lock.acquire()
        data = [r.get_display_data() for r in self.__resources]
        self.lock.release()

        headers = ['prefered', 'has local', 'name', 'timestamp']
        return tabulate(data, headers=headers)

    @synchronized
    def clear(self):
        self.__timestamp = time()
        self.__resources = []

    @synchronized
    def remove(self, address):
        self.__timestamp = time()
        for resource in self.__resources:
            resource.remove(address)

        self.__resources = [res for res
                            in self.__resources
                            if not res.is_empty()]
