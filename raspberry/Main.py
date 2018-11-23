#!/usr/bin/env python
import time

from DataBase import DataBase
from TcpClient import TcpClient
from TcpServer import TcpServer
from Gsm import Gsm
from Nrf import Nrf

#room1$TV/12/1$cooler/13/0@room2$lamp/14/1$ dimer/15/150
# add a room addroom/room1
# rename a room rnmroom/room1/room3 ||
# remove a room rmroom/room3
# add a module addm/room/TV/123
# rename module rnmm/TV/fan
# chage module id changeid/123/321
# change value changeval/123/100 : first one is id and second is val
# remove module rmm/123
# {R,M}/USER/PASS/command/{}

time.sleep(10)

host = "217.79.184.161"
port = 12345

dataBaseFileName = "database"
userPassFileName = "userpass"

Nrf = Nrf()
Nrf.start()
print("Nrf is ok")

db = DataBase(dataBaseFileName, userPassFileName, Nrf)
db.open()
db.read()
db.readUserPass()

print("database is ok")

threadServer = TcpServer(db)
threadServer.start()

print('tcpServer is ok')
threadClient = TcpClient(host, port,db)
threadClient.start()
#time.sleep(5000)
print("tcpclient is ok")

threadGsm = Gsm(db)
threadGsm.start()
print("Gsm is ok")
time.sleep(5000)








'''
while not fup:
    read_sockets, write_sockets, error_sockets = select.select(commun.CONNECTION_LIST, [], [])
    for sock in read_sockets:
        if fup:
            break
        # New connection
        if sock == socket.socketTcp:
            # Handle the case in which there is a new connection recieved through wifi
            sockfd, addr = socket.socketTcp.accept()
            socket.CONNECTION_LIST.append(sockfd)
            socket.user_list.append(sockfd)
            print(sockfd, "  ")
            print("Client (%s, %s) connected" % addr)
        # Some incoming message from a client
        else:
            # Data recieved from client, process it
            try:
                data = str(sock.recv(commun.BUFFER_SIZE))
                if data:

                    print("testing ")
                    print(db.datasheet)
                    print(db.strdata)
                    data = str(data)[2:len(data) - 1]
                    print("data is " + data)

                    # read manually the data base file
                    if db.checkup(data, 'read'):
                        print("ok read it")
                        db.open()
                        db.read()

                        # get database
                    elif db.checkup(data, 'get'):
                        print("ok get it")
                        sock.send(db.strdata.encode())


                    # exit
                    elif db.checkup(data, 'exit'):
                        fup = True
                        break

                    elif db.checkup(data, 'write'):
                        db.write()
                        break

                    elif db.domessage(data):
                        sendallip(data, sock)

                    else:
                        print('wrong data form')
                        sock.send(('wrong data form').encode())
                        # client disconnected, so remove from socket list
            except:
                print(' fup : ', sys.exc_info())
                print("some thing get fup")
                print("Client (%s, %s) is offline" % addr)
                sock.close()
                commun.CONNECTION_LIST.remove(sock)
                commun.user_list.remove(sock)
                continue

commun.wifi.close()

'''



# getting data base
'''          
          if data == 'getdb':
            sock.send(db.strdata.encode())
          #update a sensor : update1234@1
          elif checkup(data, 'update'):
            data = str(data)[6:len(data)]
            temp_switch = False
            temp_id = ''
            temp_state = ''
            for x in data:
              if x == '@':
                temp_switch = True
              elif temp_switch:
                temp_state += x
              else:
                temp_id += x
            
            for room in db.datasheet:
              room_col = 0
              while room_col < len(room):
                if (room_col % 3) == 2:
                  if room[room_col] == temp_id:
                    room[room_col + 1] = temp_state


                room_col += 1

          #delete a room : deleteroomroom1
          elif checkup(data, 'deleteroom'):
            data = str(data)[10:len(data)]
          #delete sensor : deletesens123
          elif checkup(data, 'deletesens'):
            data = str(data)[10:len(data)]
          #newroom : newroomroom1
          elif checkup(data, 'newroom'):
            data = str(data)[3:len(data)]
          #newsens : newsensroom1$tv,321@1
          elif checkup(data, 'newsens'):
            data = str(data)[7:len(data)]





            db.strdata = data
            db.str2list()
            db.write()
            for temp_sock in commun.user_list:
                print(" he get update ", temp_sock)
                temp_sock.send(db.strdata.encode())
            #commun.micro.write(str(data).encode())
            #x = commun.micro.readline()
          
  '''
