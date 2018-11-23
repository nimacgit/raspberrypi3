import threading

from ServerDB import *
from CommandCompute import *


class ClientHandler(threading.Thread):
    def __init__(self, tcpsocket, addr, server, database):
        threading.Thread.__init__(self)
        self.server = server
        self.dataBase = database
        self.addr = addr
        self.BUFFER_SIZE = 2048
        self.tcpSocket = tcpsocket
        self.id = -1


    def run(self):
        while True:
            try:
                self.data = str(self.tcpSocket.recv(self.BUFFER_SIZE).decode())
                self.commandList = getCommand(self.data)
                if len(self.commandList) >= 3:
                    print("data is " + self.data)
                    self.id = self.dataBase.findUserId(self.commandList[1], self.commandList[2])
                    if (self.id != -1):
                        self.dataBase.domessage(self.commandList, self.tcpSocket, self.commandList[1], self.commandList[2] , self.id)

                    else:
                        self.tcpSocket.send("wrong userpass".encode())
                else:
                    self.tcpSocket.send("wrong data form".encode())

            except:
                print("Client (%s, %s) is offline" % self.addr)
                self.tcpSocket.close()
                return
