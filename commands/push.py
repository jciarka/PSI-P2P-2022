import argparse
from commands.errors import InvalidCommandError


class Push:
    def __init__(self, args) -> None:
        parser = self.__getParser()

        try:
            self.args = parser.parse_args(args)
        except SystemExit:
            raise InvalidCommandError()

    def __getParser(self):
        parser = argparse.ArgumentParser(
            "Command ls")

        parser.add_argument(
            "-r", "--resource", nargs='*', type=str, required=True)
        parser.add_argument(
            "-d", "--directory", type=list, required=True)

        return parser

    def execute(self, client):
        raise NotImplementedError()