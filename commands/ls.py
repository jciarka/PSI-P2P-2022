import argparse


class Ls():
    def __init__(self, args) -> None:
        parser = self.__getParser()
        try:
            self.args = parser.parse_args(args)
        except SystemExit as ex:
            print(ex)

        print(self.args.local)

    def __getParser(self):
        parser = argparse.ArgumentParser(
            "Command ls")

        parser.add_argument("-l", "--local", action='store_true')
        return parser

    def execute(self, client):
        items, errors = client.get_resources_info()
