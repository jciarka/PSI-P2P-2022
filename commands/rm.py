import argparse
from commands.errors import InvalidCommandError


class Rm:
    def __init__(self, args) -> None:
        parser = Rm.__getParser()

        try:
            self.args = parser.parse_args(args)
        except SystemExit:
            raise InvalidCommandError()

    @staticmethod
    def __getParser():
        parser = argparse.ArgumentParser(
            "Command RM", description="removes resource")

        parser.add_argument(
            "-s", "--resource", nargs='*', type=str, required=True)

        return parser

    @staticmethod
    def print_usage():
        return Rm.__getParser().print_help()

    def execute(self, client):
        raise NotImplementedError()
