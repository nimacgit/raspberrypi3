from TcpServer import TcpServer
from UpdateRasp import UpdateRasp
from ServerDB import ServerDB

port = 12345

dataBaseFileName = "RPI"
userPassFileName = "UserPass"

db = ServerDB(dataBaseFileName, userPassFileName)
#db.open()
#db.read()
#db.readUserPass()




print("database is ok")

threadServer = TcpServer(db)
threadServer.start()
print('tcpServer is ok')

threadRasp = UpdateRasp(db)
threadRasp.start()
print('updateRasp is ok')

