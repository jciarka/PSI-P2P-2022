import argparse
from commands.errors import InvalidCommandError
from config import DEFAULT_RESOURCE_PATH, LOCAL_RESOURCE_ADDRESS
from infrastructure.resources import Resources
from infrastructure.resource import Resource
import shutil


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


        return parser

    @staticmethod
    def print_usage():
        return Push.__getParser().print_help()

    def execute(self, client, resources: Resources,
                resource_path=DEFAULT_RESOURCE_PATH):
        try:
            shutil.copy2(self.args.resource[0], resource_path)
            print("File pushed successfully.")

        except IndexError:
            print("Invalid name")
        # If source and destination are same
        except shutil.SameFileError:
            print("Source and destination represents the same file.")

        # If destination is a directory.
        except IsADirectoryError:
            print("Destination is a directory.")

        # If there is any permission issue
        except PermissionError:
            print("Permission denied.")

        # For other errors
        except:
            print("Error occurred while pushing file.")
