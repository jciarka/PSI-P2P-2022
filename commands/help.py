import argparse
from commands.errors import InvalidCommandError


class Help():
    def __init__(self, registered_commands, args) -> None:
        parser = Help.__getParser()
        try:
            self.args = parser.parse_args(args)
        except SystemExit:
            raise InvalidCommandError()

        self.__commands = registered_commands

    @staticmethod
    def __getParser():
        parser = argparse.ArgumentParser(
            "Command help", description="prints help")
        return parser

    @staticmethod
    def print_usage():
        return Help.__getParser().print_usage()

    def execute(self, client=None, resources=None, resource_path=None):
        for command in self.__commands:
            command.print_usage()
            print('\n\n')
