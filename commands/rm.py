import argparse
from commands.errors import InvalidCommandError


class Rm:
    def __init__(self, args) -> None:
        parser = self.__getParser()

        try:
            self.args = parser.parse_args(args)
        except SystemExit:
            raise InvalidCommandError()

    def __getParser(self):
        parser = argparse.ArgumentParser(
            "Command rm")

        parser.add_argument(
            "-s", "--resource", nargs='*', type=str, required=True)

        return parser

    def execute(self, client):
        raise NotImplementedError()
