class TCPClient():

    def __init__(self, host, port, retryAttempts=10):
        # this is the constructor that takes in host and port. retryAttempts is given
        # a default value but can also be fed in.
        self.host = host
        self.port = port
        self.retryAttempts = retryAttempts
        self.socket = None

    def connect(self, attempt=0):
        if attempts < self.retryAttempts:
            # put connecting code here
        if connectionFailed:
            self.connect(attempt+1)

    def diconnectSocket(self):
        # perform all breakdown operations
        ...
        self.socket = None

    def sendDataToDB(self, data):
        # send data to db

    def readData(self):
        # read data here
        while True:
            if self.socket is None:
                self.connect()
            ...
