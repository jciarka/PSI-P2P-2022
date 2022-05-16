from commands.ls import Ls
from commands.fetch import Fetch
from commands.push import Push
from commands.rm import Rm
from commands.errors import InvalidCommandError


class CommandsFactory:
    @staticmethod
    def resolve(command_str):
        command, *args = command_str.split(' ')

        if len(command) == 0:
            raise InvalidCommandError()

        if command == Ls.__name__.lower():
            return Ls(args)

        if command == Push.__name__.lower():
            return Push(args)

        if command == Fetch.__name__.lower():
            return Fetch(args)

        if command == Rm.__name__.lower():
            return Rm(args)

        return None
