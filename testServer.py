import socket

import sys
import threading

import time


class TcpClientRecive(threading.Thread):
    def __init__(self, socket):
        threading.Thread.__init__(self)
        self.socketTcp = socket

    def run(self):
        while True:
            try:
                self.data = self.socketTcp.recv(1024).decode()
                if(self.data != ""):
                    print(self.data)
            except:
                pass
            time.sleep(1)


host = "192.168.0.1"
vhost = "217.79.184.161"
port = 12345

while True:

    try:
        socketTcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socketTcp.connect((host, port))
        print("connected")
    except socket.error:
        print('Failed to create socket')
        sys.exit()
    try:
        threadRec = TcpClientRecive(socketTcp)
        threadRec.start()
        while True:
            a = input()
            socketTcp.send(a.encode())
    except:
        print("cant connect")
