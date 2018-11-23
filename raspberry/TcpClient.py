import socket   
import sys
import threading

import time
from commandCompute import getCommand


class TcpClient(threading.Thread):
    def __init__(self, ip, port, database):
        threading.Thread.__init__(self)
        self.host = ip
        self.port = port
        self.dataBase = database

    def run(self):
        #create an INET, STREAMing socket
        try:
            self.socketTcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error:
            print('Failed to create socket')
            sys.exit()
        print('Socket Created')
        while True:
            try:
                self.remote_ip = socket.gethostbyname( self.host )
                self.socketTcp.connect((self.host, self.port))
                print('Socket Connected to ' + self.host + ' on ip ' + self.remote_ip)
                #debugoo
                self.socketTcp.send("R/1/blueberry/login".encode())
                while True:
                    while len(self.dataBase.vpsLog) > 0:
                        self.socketTcp.send(self.dataBase.vpsLog[0].encode())
                        self.dataBase.vpsLog.pop(0)
                    try:
                        self.data = self.socketTcp.recv(1024).decode()
                    except:
                        print("disconnected from server")
                    print(" I get : " + self.data)
                    self.commandList = getCommand(self.data)
                    if len(self.commandList) >= 3:
                        if (self.dataBase.USERNAME == self.commandList[1] and self.dataBase.PASSWORD ==
                                self.commandList[2]):
                            self.dataBase.domessage(self.commandList, self.socketTcp)
                        else:
                            print("wrong userpass")
                            self.socketTcp.send("wrong userpass".encode())
            except:
                print('Hostname could not be resolved')
            time.sleep(3)







    '''
    try :
        t1 = time.time()
        s.send(message.encode())
        t2 = time.time()
        print(str(t2 - t1) + " ms took send")
        print('Message sent successfully')
    except socket.error:
        print('Send failed')
    t1 = time.time()
    data = s.recv(1024)
    t2 = time.time()
    print(str(t2 - t1) + " ms took read1")
    print(data.decode())
    t1 = time.time()
    data = s.recv(1024)
    t2 = time.time()
    print(str(t2 - t1) + " ms took read2")
    print(data.decode())

    '''
    '''
    def recv_timeout(the_socket,timeout=2):
        #make socket non blocking
        the_socket.setblocking(0)
    
        #total data partwise in an array
        total_data=[];
        data='';
    
        #beginning time
        begin=time.time()
        while 1:
            #if you got some data, then break after timeout
            if total_data and time.time()-begin > timeout:
                break
    
            #if you got no data at all, wait a little longer, twice the timeout
            elif time.time()-begin > timeout*2:
                break
    
            #recv something
            try:
                data = the_socket.recv(8192)
                if data:
                    total_data.append(data)
                    #change the beginning time for measurement
                    begin=time.time()
                else:
                    #sleep for sometime to indicate a gap
                    time.sleep(0.1)
            except:
                pass
    
        #join all parts to make final string
        return ''.join(total_data)
    
    #get reply and print
    print recv_timeout(s)
    '''
#s.close()
