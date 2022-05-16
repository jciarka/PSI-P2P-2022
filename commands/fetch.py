import argparse
from commands.errors import InvalidCommandError


class Fetch:
    def __init__(self, args) -> None:
        parser = Fetch.__getParser()

        try:
            self.args = parser.parse_args(args)
        except SystemExit:
            raise InvalidCommandError()

        if not self.args or (not self.args.file and not self.args.directory):
            print("""usage: Command ls [-h] [-f [FILE [FILE ...]]] [-d DIRECTORY]
Command ls: error: one of direcotry or file must be provided""")
            raise InvalidCommandError

    @staticmethod
    def __getParser():
        parser = argparse.ArgumentParser(
            "Command FETCH", description="downloads resource")
        parser.add_argument("-f", "--file", nargs='*', type=str)
        parser.add_argument("-d", "--directory", type=list)

        return parser

    @staticmethod
    def print_usage():
        return Fetch.__getParser().print_help()

    def validateInput(self):
        if not self.args:
            print()

    def execute(self, client):
        raise NotImplementedError()
