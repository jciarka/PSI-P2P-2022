# from os import listdir
# from os.path import isfile, join, getmtime
from config import InjectionContainer, FILE_TRANSFER_PORT
# from infrastructure.local_resources_util import LocalResourcesUtil


class SendFileAction:
    def __init__(self, connection, address) -> None:
        self.__connection = connection,
        self.__address = address

    def execute(self):
        s = socket.socket()         # Create a socket object
        host = socket.gethostname() # Get local machine name
        port = 12345                 # Reserve a port for your service.
        s.bind((host, port))        # Bind to the port
        desired_file = '' ## TODO desired file name
        f = open(desired_file,'wb')
        s.listen(5)                 # Now wait for client connection.
        while True:
            c, addr = s.accept()     # Establish connection with client.
            print 'Got connection from', addr
            print "Receiving..."
            l = c.recv(1024)
            while (l):
                print "Receiving..."
                f.write(l)
                l = c.recv(1024)
            f.close()
            print "Done Receiving"
            c.send('Thank you for connecting')
            c.close()                # Close the connection
        # serializer = InjectionContainer["serializer"]
        # data = serializer.deserialzie(body)

        # TODO: implement response for send file requirement

        pass
        # wywłanie pliku
