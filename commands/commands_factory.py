from commands.ls import Ls
from commands.fetch import Fetch
from commands.push import Push
from commands.rm import Rm
from commands.exit import Exit
from commands.help import Help
from commands.pull import Pull
from commands.errors import InvalidCommandError


registered_commands = [
    Ls, Fetch, Push, Rm, Exit, Help, Pull
]


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

        if command == Help.__name__.lower():
            return Help(registered_commands, args)

        if command == Exit.__name__.lower():
            return Exit(args)
        
        if command == Pull.__name__.lower():
            return Pull(args)

        return None
