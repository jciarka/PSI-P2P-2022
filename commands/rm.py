import argparse
from commands.errors import InvalidCommandError
from config import DEFAULT_RESOURCE_PATH
from infrastructure.resources import Resources
import os


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
            "-f", "--file", nargs='*', type=str, required=False)
        parser.add_argument(
            "-d", "--directory", nargs='*', type=str, required=False)

        return parser

    @staticmethod
    def print_usage():
        return Rm.__getParser().print_help()

    def execute(self, client, resources: Resources,
                resource_path=DEFAULT_RESOURCE_PATH):
        if self.args.file and self.args.directory:
            print("You cannot use both file and directory")
        if self.args.file:
            if os.path.exists(resource_path + '/' + self.args.file[0]) \
                    and len(self.args.file[0]):
                os.remove(resource_path + '/' + self.args.file[0])
            else:
                print("The file does not exist")
        if self.args.directory:
            if os.path.exists(resource_path + '/' + self.args.directory[0]) \
                    and len(self.args.directory[0]):
                os.rmdir(resource_path + '/' + self.args.directory[0])
            else:
                print("The directory does not exist")
        else:
            self.print_usage()
