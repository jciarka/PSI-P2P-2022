import argparse
from commands.errors import InvalidCommandError


class Push:
    def __init__(self, args) -> None:
        parser = Push.__getParser()

        try:
            self.args = parser.parse_args(args)
        except SystemExit:
            raise InvalidCommandError()

    @staticmethod
    def __getParser():
        parser = argparse.ArgumentParser(
            "Command PUSH", description="addes or updates resource")

        parser.add_argument(
            "-r", "--resource", nargs='*', type=str, required=True)
        parser.add_argument(
            "-d", "--directory", type=list, required=True)

        return parser

    @staticmethod
    def print_usage():
        return Push.__getParser().print_help()

    def execute(self, client):
        raise NotImplementedError()
