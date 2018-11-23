import socket
import threading, time

class UpdateRasp(threading.Thread):
    def __init__(self, database):
        threading.Thread.__init__(self)
        self.dataBase = database

    def run(self):
        while True:
            i = 1
            while i < len(self.dataBase.raspList):
                rasplist = self.dataBase.raspList[i]
                for sockf in rasplist:
                    try:
                        print(" send update command to this rasp ", sockf.getpeername())
                        message = "R/" + str(i) + "/" + str(self.dataBase.findUserPass(i)) + "/get"
                        sockf.send(message.encode())
                    except:
                        print("cant send client message to rasp")
                        rasplist.remove(sockf)
                        sockf.close()
                time.sleep(4)
