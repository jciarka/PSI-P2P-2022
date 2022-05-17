import argparse
from commands.commands_factory import CommandsFactory
from client.client import Client
from services.catalog.catalog_service import CatalogService
from services.catalog.catalog_publisher import CatalogPublisher
import threading
from infrastructure.resources import Resources
from commands.ls import get_all_resources
from commands.errors import InvalidCommandError, ShutDownSystemError
from config import VERSION, RESOURCE_GROUP_ID, DEFAULT_RESOURCE_PATH, \
    CATALOG_PUBLISHER_AWAKE_PERIOD, CATALOG_PUBLISHER_SEND_PERIOD

parser = argparse.ArgumentParser(
    "The program reads the text form file and converts in using" +
    "enigma macine model which implementation details are imported" +
    "form settings_file")

parser.add_argument("-p", "--path",
                    default=DEFAULT_RESOURCE_PATH,
                    help="path to resources that uou want to share")
parser.add_argument("-d", "--delay",
                    type=int,
                    default=2,
                    help="Time in seconds that cilient will wait for serwer answers")
parser.add_argument("-a", "--awake_period",
                    type=int,
                    default=CATALOG_PUBLISHER_AWAKE_PERIOD,
                    help="Publisher awake period in seconds")
parser.add_argument("-s", "--publish_period",
                    type=int,
                    default=CATALOG_PUBLISHER_SEND_PERIOD,
                    help="Publishing period in second")
parser.add_argument("-g", "--group",
                    type=int,
                    default=RESOURCE_GROUP_ID,
                    help="Unique id of group in local network")

args = parser.parse_args()

# set up resources and request data
client = Client(args.delay, VERSION, args.group)
resources = Resources()
get_all_resources(client, args.path, resources)

# set up catalog service
catalog_server = CatalogService(resources, args.path)

catalog_server_thread = threading.Thread(
    target=catalog_server.run)

catalog_server_thread.start()

# set up catalog publisher
catalog_publisher = CatalogPublisher(
    VERSION,
    args.path,
    args.group,
    args.awake_period,
    args.publish_period)

catalog_publisher_thread = threading.Thread(
    target=catalog_publisher.run)

catalog_publisher_thread.start()

# TO DO: set up transfer service


# command loop
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

# free services and publisher
catalog_server.cancelation_token = True
catalog_publisher.cancelation_token = True
print("Turning off services...")

catalog_server_thread.join()
catalog_publisher_thread.join()
print("Goodbye")
