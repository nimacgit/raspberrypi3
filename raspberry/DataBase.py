#!/usr/bin/env python
from commandCompute import *
import socket
###from raspberry.Nrf import Nrf

class DataBase:
    ''' room1 $ tv , 123 @ on / room2 ...
    '''

    def __init__(self, filename, userpassFile, nrf):
        self.name = str(filename)
        self.userpassFile = str(userpassFile)
        self.datasheet = []
        self.strdata = ''
        self.USERNAME = ""
        self.PASSWORD = ""
        self.CONNECTION_LIST = []
        self.vpsLog = []
        self.nrf = nrf

    def sendallip(self, message):
        for sockf in self.CONNECTION_LIST:
            try:
                print(" he get update ", sockf.getpeername())
                sockf.send(message.encode())
            except socket.error:
                self.CONNECTION_LIST.remove(sockf)
                sockf.close()


    def open(self):
        self.ostream = open(self.name, 'r')

    def str2list(self):
        inp = self.strdata
        cut_temp = ''
        list_temp = []
        self.datasheet = []
        for x in inp:
            if (x == '$') or (x == '/'):
                list_temp.append(cut_temp)
                cut_temp = ''
            elif x == '@':
                list_temp.append(cut_temp)
                self.datasheet.append(list_temp)
                cut_temp = ''
                list_temp = []
            else:
                cut_temp += x
        if len(list_temp) > 0:
            self.datasheet.append(list_temp)

    def list2str(self):
        self.strdata = ''

        for room in self.datasheet:
            self.strdata += str(room[0])
            temp_room = room[:]
            temp_room.pop(0)
            while temp_room:
                self.strdata += str('$' + temp_room[0] + '/' + temp_room[1] + '/' + temp_room[2])
                temp_room.pop(0)
                temp_room.pop(0)
                temp_room.pop(0)
            self.strdata += '@'

    def readUserPass(self):
        self.ostreamUserPass = open(self.userpassFile, 'r')
        self.userPass = getCommand(str(self.ostreamUserPass.read()))
        self.ostreamUserPass.close()
        self.USERNAME = self.userPass[0]
        self.PASSWORD = self.userPass[1]

    def writeUserPass(self):
        self.istreamUserPass = open(self.userpassFile, 'w')
        self.istreamUserPass.write(self.USERNAME + "/" + self.PASSWORD)
        self.istreamUserPass.close()

    def read(self):
        self.strdata = str(self.ostream.read())
        self.str2list()
        self.ostream.close()

    def write(self):
        self.istream = open(self.name, 'w')
        self.istream.write(self.strdata)
        self.istream.close()

    def checkup(self, inp, keyword):
        if len(inp) < len(keyword):
            return False
        n = len(keyword)
        i = 0
        while i < n:
            if keyword[i] != inp[i]:
                return False
            i += 1
        return True

    def domessage(self, commandList, tcpSocket):
        # get database
        if commandList[3] == "get" and tcpSocket != "null":
            print("get db")
            try:
                tcpSocket.send(("R/" + self.USERNAME + "/" + self.PASSWORD + "/set/" + self.strdata).encode())
            except:
                "cant send (do message)"
        elif commandList[3] == 'set':
            print("ok seting")
            self.strdata = commandList[4]
            self.str2list()

        elif commandList[3] == 'setuserpass':
            self.USERNAME = commandList[4]
            self.PASSWORD = commandList[5]
            self.writeUserPass()
        elif commandList[3] == 'login' and tcpSocket != "null":
            self.CONNECTION_LIST.append(tcpSocket)
        elif commandList[3] == 'logout' and tcpSocket != "null":
            self.CONNECTION_LIST.remove(tcpSocket)

        # add a room addroom/room1
        else:
            if commandList[3] == "addroom":
                self.datasheet.append([commandList[4]])

            # rename a room rnmroom/room1/room3 ||
            elif commandList[3] == 'rnmroom':
                for room in self.datasheet:
                    if room[0] == commandList[4]:
                        room[0] = commandList[5]
                        break

                # remove a room rmroom/room3
            elif commandList[3] == 'rmroom':
                for room in self.datasheet:
                    if room[0] == commandList[4]:
                        self.datasheet.remove(room)
                        break

            # add a module addm/room/TV/123
            elif commandList[3] == 'addm':
                done = False
                for room in self.datasheet:
                    if room[0] == commandList[4]:
                        room.append(commandList[5])
                        room.append(commandList[6])
                        room.append('0')
                        done = True
                        break
                if not done:
                    self.datasheet.append([commandList[4], commandList[5], commandList[6], '0'])


            # rename module rnmm/TV/fan
            elif commandList[3] == 'rnmm':
                i = 0
                while i < len(self.datasheet):
                    room = self.datasheet[i]
                    j = 1
                    while j < len(room):
                        if room[j] == commandList[4]:
                            self.datasheet[i][j] = commandList[5]
                            break
                        j += 3
                    i += 1

            # chage module id changeid/123/321
            elif commandList[3] == 'changeid':
                i = 0
                while i < len(self.datasheet):
                    room = self.datasheet[i]
                    j = 2
                    while j < len(room):
                        if room[j] == commandList[4]:
                            self.datasheet[i][j] = commandList[4]
                            break
                        j += 3
                    i += 1

            # change value changeval/123/100 : first one is id and second is val
            elif commandList[3] == 'changeval':
                i = 0
                while i < len(self.datasheet):
                    room = self.datasheet[i]
                    j = 2
                    while j < len(room):
                        if room[j] == commandList[4]:
                            self.nrf.send(commandList[5], commandList[4])
                            self.datasheet[i][j + 1] = commandList[5]
                            break
                        j += 3
                    i += 1

            # remove module rmm/123
            elif commandList[3] == 'rmm':
                i = 0
                while i < len(self.datasheet):
                    j = 2
                    room = self.datasheet[i]
                    while j < len(room):
                        if room[j] == commandList[4]:
                            self.datasheet[i].pop(j - 1)
                            self.datasheet[i].pop(j - 1)
                            self.datasheet[i].pop(j - 1)
                            break
                        j += 3
                    i += 1

            elif tcpSocket != "null":
                tcpSocket.send("wrong data form".encode())
                return
            commandList[0] = 'R'
            self.sendallip(getStr(commandList))
            commandList[0] = "L"
            self.vpsLog.append(getStr(commandList))
            self.list2str()
            self.write()


    def __del__(self):
        print("destroyed")
