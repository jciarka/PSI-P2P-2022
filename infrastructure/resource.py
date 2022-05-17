from tabulate import tabulate
from datetime import datetime
from config import LOCAL_RESOURCE_ADDRESS


class Resource():
    @property
    def name(self):
        return self.__name

    @property
    def addresses(self) -> list:
        return [addr for addr, _ in self.__timed_addresses]

    @property
    def addresses_with_timestamp(self) -> list:
        return [(addr, time) for addr, time in self.__timed_addresses]

    @property
    def prefered_address(self) -> str:
        sorted_data = sorted(self.__timed_addresses,
                             key=lambda x: x[1], reverse=True)
        return sorted_data[0][0] if len(sorted_data) > 0 else None

    @property
    def prefered_timestamp(self) -> float:
        sorted_data = sorted(self.__timed_addresses,
                             key=lambda x: x[1], reverse=True)
        return sorted_data[0][1] if len(sorted_data) > 0 else None

    @property
    def is_valid(self):
        return self.prefered_address is not None and\
            self.prefered_timestamp is not None

    def get_display_data(self) -> str:
        if not self.is_valid:
            return None

        data = []
        data.append('local' if self.prefered_address ==
                    LOCAL_RESOURCE_ADDRESS else 'remote')
        data.append('yes' if LOCAL_RESOURCE_ADDRESS
                    in self.addresses else 'no')
        data.append(self.name)
        data.append(datetime.fromtimestamp(self.prefered_timestamp)
                    .strftime("%Y-%m-%d %H:%M:%S"))
        return data

    def __str__(self) -> str:
        if not self.is_valid:
            return ''

        headers = ['prefered', 'has local', 'name', 'timestamp']
        return tabulate([self.get_display_data()], headers=headers)

    def __init__(self, name) -> None:
        self.__name = name
        self.__timed_addresses = []

    def append(self, address, timestamp):
        self.__timed_addresses.append((address, timestamp))

    def remove(self, address):
        self.__timed_addresses = \
            [item for item in self.__timed_addresses
             if item[0] != address]

    def is_empty(self):
        return len(self.__timed_addresses) == 0

    def clear(self):
        self.__lock.acquire()
        self.__timed_addresses.clear()
