import threading


class ServerHandler(threading.Thread):
    def __init__(self, tcpsocket, database):
        threading.Thread.__init__(self)
        self.dataBase = database
        self.BUFFER_SIZE = 1024
        self.socketTcp = tcpsocket

    def run(self):

        while True:
            self.data = self.socketTcp.recv(1024).decode()
            print(" I get : " + self.data)
            self.commandList = getCommand(self.data)
            if len(self.commandList) >= 3:
                self.commandList = getCommand(self.data)
                if (self.dataBase.USERNAME == self.commandList[1] and self.dataBase.PASSWORD == self.commandList[2]):
                    self.dataBase.domessage(self.commandList, self.socketTcp)
                else:
                    self.socketTcp.send("wrong userpass".encode())
