import argparse
from commands.commands_factory import CommandsFactory
from client.client import Client
from services.catalog.catalog_service import CatalogService
import threading
from client.resources import Resources
from commands.errors import InvalidCommandError, ShutDownSystemError

parser = argparse.ArgumentParser(
    "The program reads the text form file and converts in using" +
    "enigma macine model which implementation details are imported" +
    "form settings_file")

parser.add_argument("-p", "--path",
                    help="path to resources that uou want to share")
parser.add_argument("-e", "--expiration",
                    type=int,
                    default=120,
                    help="Time in seconds that gathered info is teated as valid"
                    )
parser.add_argument("-d", "--delay",
                    type=int,
                    default=2,
                    help="Time in seconds that cilient will wait for serwer answers")

args = parser.parse_args()

client = Client(args.delay, args.expiration)
catalog_server = CatalogService()
catalog_server_thread = threading.Thread(target=catalog_server.run)
catalog_server_thread.start()

resources = Resources()

while True:
    command = input("?:")

    try:
        handler = CommandsFactory.resolve(command)
    except InvalidCommandError:
        continue

    if handler is None:
        print(f"Command '{command}' not found." +
              " Use help to check the wright syntax.")
        continue

    try:
        handler.execute(client, resources)
    except ShutDownSystemError:
        break

catalog_server.cancelation_token = True
print("Turning of services...")

catalog_server_thread.join()
print("Goodbye")
