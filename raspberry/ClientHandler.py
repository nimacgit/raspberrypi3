import threading

from DataBase import *


class ClientHandler(threading.Thread):
    def __init__(self, tcpsocket, addr, server, database):
        threading.Thread.__init__(self)
        self.server = server
        self.dataBase = database
        self.addr = addr
        self.BUFFER_SIZE = 1024
        self.tcpSocket = tcpsocket


    def run(self):
        while True:
            try:
                self.data = str(self.tcpSocket.recv(self.BUFFER_SIZE).decode())
                self.commandList = getCommand(self.data)
                if len(self.commandList) >= 3:
                    print("data is " + self.data)
                    print(self.commandList)
                    if ((self.dataBase.USERNAME == self.commandList[1]) and (self.dataBase.PASSWORD == self.commandList[2])):
                        self.dataBase.domessage(self.commandList, self.tcpSocket)
                    else:
                        self.tcpSocket.send("wrong userpass".encode())
                else:
                    self.tcpSocket.send("wrong data form".encode())

            except:
                print("Client (%s, %s) is offline" % self.addr)
                self.tcpSocket.close()
                return
