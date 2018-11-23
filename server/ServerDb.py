import pymongo
from CommandCompute import *
import socket




class ServerDB:
    ''' room1 $ tv , 123 @ on / room2 ...
    '''

    def __init__(self, dbName, userPassName):
        self.dataBaseName = dbName
        self.userPassName = userPassName
        self.client = pymongo.MongoClient()
        self.dataBase = self.client[str(self.dataBaseName)]
        self.userPass = self.client[str(self.userPassName)]
        self.clientList = []
        self.raspList = []
        self.logEvent = []
        for i in range(1, len(self.dataBase.list_collection_names()) + 1):
            self.clientList.append([])
            self.raspList.append([])


    def findUserId(self, user, passwrd):

        if (user in self.userPass.collection_names()):

            if(self.userPass[user].find_one({"passWord":passwrd}) != None):
                return self.userPass[user].find_one({"passWord":passwrd})['id']
        return -1

    def findUserPass(self, address):
        if (str(address) in self.userPass.collection_names()):
                return self.userPass[str(address)].find_one({'id':str(address)})['passWord']


    def sendallip(self, message, address):
        for sockf in self.clientList[int(address)]:
            try:
                print(" he get update ", sockf.getpeername())
                sockf.send(message.encode())
            except socket.error:
                self.clientList[int(address)].remove(sockf)
                sockf.close()
    def sendRasp(self,  message, address):

        if len(self.raspList[int(address)]) > 0:
            for sockfd in self.raspList[int(address)]:
                try:
                    print(" send client command to this rasp ", sockfd.getpeername())
                    sockfd.send(message.encode())
                except:
                    print("cant send client message to rasp")
                    self.raspList[int(address)].remove(sockfd)
                    sockfd.close()




    def addDBByMongo(self, user, dataList):
        user.insert({'roomname': dataList[0],
                     'module': []})
        i = 1
        while i < len(dataList):
            user.update({'roomname': dataList[0]},
                {'$push': {'module': {'name': dataList[i], 'address': dataList[i + 1], 'value': dataList[i + 2]}}})
            i += 3


    def str2list(self, strdata, address):
        user = self.dataBase[self.dataBaseName + str(address)]
        user.delete_many({})
        user.insert({'id': str(address)})
        cut_temp = ''
        list_temp = []
        for x in strdata:
            if (x == '$') or (x == '/'):
                list_temp.append(cut_temp)
                cut_temp = ''
            elif x == '@':
                list_temp.append(cut_temp)
                try:
                    self.addDBByMongo(user, list_temp)
                except:
                    print("cant do str2list1")
                cut_temp = ''
                list_temp = []
            else:
                cut_temp += x
        if(len(cut_temp) > 0):
            list_temp.append(cut_temp)
        if len(list_temp) > 0:
            try:
                print(list_temp)
                self.addDBByMongo(user, list_temp)
            except:
                print("cant do str2list2")


    def list2str(self, address):
        strdata = ''

        cursor = self.dataBase[self.dataBaseName + str(address)].find()

        for document in cursor:

            if document.get('id', None) == None:

                strdata += str(document['roomname'])

                for module in document['module']:

                    strdata += str('$' + str(module['name']) + '/' + str(module['address']) + '/' + str(module['value']))
                strdata += '@'

        return str(strdata)


    def writeUserPass(self):
        self.istreamUserPass = open(self.userpassFile, 'w')
        self.istreamUserPass.write(self.USERNAME + "/" + self.PASSWORD)
        self.istreamUserPass.close()




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

    def domessage(self, commandList, tcpSocket, userName, passwrd, address):
        # get database
        if len(commandList) < 4:
            return
        if commandList[0] == "L":
            return
        if commandList[3] == "get" and tcpSocket != "null":
            tcpSocket.send(("R/" + str(userName) + "/" + str(passwrd) + "/set/" + str(self.list2str(address))).encode())

        elif commandList[3] == 'set':
            print("ok seting")
            self.strdata = getStr(commandList[4:])
            self.str2list(self.strdata, address)
            print("done setting")
        elif commandList[3] == 'setuserpass':
            TODO
            #self.USER = commandList[4]
            #self.PASSWORD = commandList[5]
            #self.writeUserPass()

        elif commandList[3] == 'login' and tcpSocket != "null":
            if commandList[0] == 'R':
                self.raspList[int(address)].append(tcpSocket)
            else:
                self.clientList[int(address)].append(tcpSocket)

        else:
            if (commandList[0] == 'R'):
                self.sendallip(getStr(commandList), address)
            elif commandList[3] == "addroom" or commandList[3] == 'rnmroom' or commandList[3] == 'rmroom' or commandList[3] == 'addm' or commandList[3] == 'rnmm' or commandList[3] == 'changeid' or commandList[3] == 'changeval'or commandList[3] == 'rmm':
                print("hi")
                self.sendRasp(getStr(commandList), address)
            elif tcpSocket != "null":
                tcpSocket.send("wrong data form".encode())
                return





    def __del__(self):
        print("destroyed")

