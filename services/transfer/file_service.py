import socket
import threading
from config import \
    FILE_TRANSFER_PORT,\
    FILE_SERVICE_TIMEOUT

from services.transfer.file_service_actions import SendFileAction


class FileService:
    @property
    def cancelation_token(self):
        return self.__cancelation_token

    @cancelation_token.setter
    def cancelation_token(self, value):
        self.__cancelation_token = value

    @property
    def resource_path(self):
        return self.__resource_path

    def __init__(self, resources, path) -> None:
        self.cancelation_token = False

        self.__resources = resources
        self.__path = path

    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('0.0.0.0', FILE_TRANSFER_PORT))

            s.settimeout(FILE_SERVICE_TIMEOUT)
            s.listen(5)

            while not self.cancelation_token:
                try:
                    connection, address = s.accept()

                    send_file_action = SendFileAction(connection, address)
                    threading.Thread(target=send_file_action.execute)
                except socket.timeout:
                    continue


if __name__ == "__main__":
    service = FileService()
    service.run()
