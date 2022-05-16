import argparse
from commands.errors import InvalidCommandError, ShutDownSystemError


class Exit():
    def __init__(self, args) -> None:
        parser = Exit.__getParser()
        try:
            self.args = parser.parse_args(args)
        except SystemExit:
            raise InvalidCommandError()

    @staticmethod
    def __getParser():
        parser = argparse.ArgumentParser(
            "Command EXIT", description="closes system")
        return parser

    @staticmethod
    def print_usage():
        return Exit.__getParser().print_help()

    def execute(self, client=None, resources=None, resource_path=None):
        raise ShutDownSystemError()
