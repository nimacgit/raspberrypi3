#!/usr/bin/env python
import threading
import socket

from ClientHandler import ClientHandler


class TcpServer(threading.Thread):
    def __init__(self, database):
        threading.Thread.__init__(self)
        self.dataBase = database
        self.TCP_IP = '0.0.0.0'
        self.TCP_PORT = 12345
        self.socketTcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socketTcp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socketTcp.bind((self.TCP_IP, self.TCP_PORT))
        self.socketTcp.listen(5)



    def run(self):
        while True:
            self.sockfd, self.addr = self.socketTcp.accept()
            print("user : " + str(self.addr) + " is connected")
            self.thread1 = ClientHandler(self.sockfd, self.addr, self, self.dataBase)
            self.thread1.start()












#
# while True:
#   read_sockets,write_sockets,error_sockets = select.select(CONNECTION_LIST,[],[])
#   for sock in read_sockets:
#     if fup:
#       break
#     #New connection
#     if sock == wifi:
#       # Handle the case in which there is a new connection recieved through wifi
#       sockfd, addr = wifi.accept()
#       CONNECTION_LIST.append(sockfd)
#       user_list.append(sockfd)
#       print(sockfd, "  ")
#       print("Client (%s, %s) connected" % addr)
#
#     else:
#
#       try:
#         data = str(sock.recv(BUFFER_SIZE))
#         if data:
#
#           print("testing ")
#           data = str(data)[2:len(data)-1]
#           print("data is " + data)
#
#           #read manually the data base file
#           if checkup(data, 'read'):
#             print("ok read it")
#             sock.send(('read it').encode())
#
#           #get database
#           elif checkup(data, 'get'):
#             print("ok get it")
#             sock.send(('get it').encode())
#
#           else:
#             print('wrong data form')
#             sock.send(('wrong data form').encode())
#         # client disconnected, so remove from socket list
#       except:
#         print(' fup : ', sys.exc_info())
#         print("some thing get fup")
#         print("Client (%s, %s) is offline" % addr)
#         sock.close()
#         CONNECTION_LIST.remove(sock)
#         user_list.remove(sock)
#         continue
#
# wifi.close()
#







