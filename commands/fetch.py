import argparse
from multiprocessing.connection import Client
from commands.errors import InvalidCommandError
from config import LOCAL_RESOURCE_ADDRESS
from infrastructure.resources import Resources


class Fetch:
    def __init__(self, args) -> None:
        parser = Fetch.__getParser()

        try:
            self.args = parser.parse_args(args)
        except SystemExit:
            raise InvalidCommandError()

        if not self.args or (not self.args.file):
            print("""usage: Command fetch [-h] [-f [FILE ]]
Command fetch: error: one of direcotry or file must be provided""")
            raise InvalidCommandError

    @staticmethod
    def __getParser():
        parser = argparse.ArgumentParser(
            "Command FETCH", description="downloads resource")
        parser.add_argument("-f", "--file", nargs='*', type=str, required=True)

        return parser

    @staticmethod
    def print_usage():
        return Fetch.__getParser().print_help()

    def validateInput(self):
        if not self.args:
            print()

    def execute(self, client: Client, resources: Resources,
                resource_path=LOCAL_RESOURCE_ADDRESS):
        if self.args.file[0]:
            timestamp = 0
            address = 0
            results, _, _ = client.get_resources_info()
            for result in results:
                if len(result[1]) and result[1][0].get('name') == self.args.file[0]:
                    if timestamp < result[1][0].get('modified'):
                        address = result[0]
                        timestamp = result[1][0].get('modified')
            if address == 0:
                print("File not found")
                return
            success = client.get_file_from_remote_host(address[0], self.args.file[0])
            if not success:
                print("File not fetched")
                return

