#!/usr/bin/env python
import RPi.GPIO as GPIO
import serial
import threading
import time

from commandCompute import getCommandGsm


class Gsm(threading.Thread):
    def setup(self):
        threading.Thread.__init__(self)
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        # GPIO.setup(23, GPIO.OUT)
        # GPIO.setup(24, GPIO.OUT)
        # GPIO.setup(25, GPIO.OUT)
        self.SERIAL_PORT = "/dev/ttyS0"
        self.baudrate = 9600
        self.timeout = 5

    def __init__(self, db):
        threading.Thread.__init__(self)
        self.dataBase = db
        self.setup()
        self.sim = serial.Serial(self.SERIAL_PORT, self.baudrate, self.timeout)
        self.sim.write(("AT+CMGF=1\r\n").encode())  # set to text mode
        time.sleep(1)
        self.reply = self.sim.read(self.sim.inWaiting()).decode()  # Clean buf
        time.sleep(1)
        print("Listening for incomming SMS... :")

    def run(self):
        self.sim.write(('AT+CMGDA="DEL ALL"\r').encode())  # delete all SMS
        time.sleep(1)
        self.sim.write(('AT+CMGDA="DEL ALL"\r').encode())  # delete all SMS
        time.sleep(1)
        self.reply = self.sim.read(self.sim.inWaiting()).decode()  # Clean buf
        while True:
            self.sim.write(("AT+CMGR=1\r").encode())
            time.sleep(1)
            self.reply = self.sim.read(self.sim.inWaiting()).decode()
            if len(self.reply) > 30:
                print(" hey replay : " + self.reply)
                self.commandList = getCommandGsm(self.reply)
                time.sleep(1)
                self.sim.write(('AT+CMGD=1\r').encode())
                time.sleep(1)
                self.reply = self.sim.read(self.sim.inWaiting()).decode()
                print("del mess : " + self.reply)
                time.sleep(1)
                self.sim.write(('AT+CMGD=1\r').encode())
                time.sleep(1)
                self.reply = self.sim.read(self.sim.inWaiting()).decode()
                print("del mess : " + self.reply)
                if len(self.commandList) >= 3:
                    print("dataGsm is " + self.reply)
                    if ((self.dataBase.USERNAME == self.commandList[1]) and (
                            self.dataBase.PASSWORD == self.commandList[2])):
                        self.dataBase.domessage(self.commandList, "null")
            time.sleep(1)


'''
    inp = input()
    if inp == "nima":
        self.text += '\r'
        sim.write(self.text.encode())
        text = ""
        time.sleep(1)
        reply = ser.read(ser.inWaiting())
        print(reply.decode())
    elif inp == "milad":
        text += (chr)(26)
        ser.write(text.encode())
        text = ""
        time.sleep(1)
        reply = ser.read(ser.inWaiting())
        print(reply.decode())
    else:
        text += inp
time.sleep(.500)
ser.write('AT+CMGDA="DEL ALL"\r'.encode())  # delete all
time.sleep(.500)
ser.read(ser.inWaiting())  # Clear buffer
time.sleep(.500)


text = ""

'''
