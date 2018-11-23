#!/usr/bin/env python
import  time,socket ,sys ,struct, bluetooth, serial


'''print(time.clock())'''

ser = serial.Serial(
  port='/dev/ttyS0',
  baudrate = 9600,
  parity=serial.PARITY_NONE,
  stopbits=serial.STOPBITS_ONE,
  bytesize=serial.EIGHTBITS,
  timeout=1
)

print(ser.portstr)
print("Serial is open: " + str(ser.isOpen()))


inputstr = input("write cmd : ")
while inputstr != "exit":
    ser.write(inputstr.encode())
    print("Now read : ")
    x = ser.readline()
    print("got '" + x.decode() + "'")
    inputstr = input("write cmd : ")



#print("checking bluetooth devices")
#devices = bluetooth.discover_devices(duration=1, lookup_names=True)
#for addr, name in devices:
#   print("bluetooth addr : " + addr + " name : " + name)



ser.close()

'''
while 1:
  read_sockets,write_sockets,error_sockets = select.select(CONNECTION_LIST,[],[])
  for sock in read_sockets:         
    #New connection
    if sock == wifi:
      # Handle the case in which there is a new connection recieved through wifi
      sockfd, addr = wifi.accept()
      CONNECTION_LIST.append(sockfd)
      print("Client (%s, %s) connected" % addr)


    #Some incoming message from a client
    else:
      # Data recieved from client, process it
      try:
          #In Windows, sometimes when a TCP program closes abruptly,
          # a "Connection reset by peer" exception will be thrown
          data = sock.recv(BUFFER_SIZE)
          # echo back the client message
          if data:

            data = str(data)[2] + str(data)[3]      
            print("data is " + data)
            micro.write(str(data).encode())
            x = micro.readline()
            print("got '" + x.decode() + "'")
            sock.send(data.encode())


      # client disconnected, so remove from socket list
      except:
          print("Client (%s, %s) is offline" % addr)
          sock.close()
          CONNECTION_LIST.remove(sock)
          continue




'''

'''conn, addr = wifi.accept()
conn.send(("hello").encode())
data = conn.recv(BUFFER_SIZE)
print('Connection address:', addr)
print("received data:", data)
if(len(str(data)) > 3):
  data = str(data)[2] + str(data)[3]
else:
  data = '00'
print("data is " + data)
micro.write(str(data).encode())
x = micro.readline()
print("got '" + x.decode() + "'")
conn.send(data.encode())

start_new_thread(client_thread ,(conn,))

print("debug")'''

# print("checking bluetooth devices")
# devices = bluetooth.discover_devices(duration=1, lookup_names=True)
# for addr, name in devices:
#    print("bluetooth addr : " + addr + " name : " + name)


