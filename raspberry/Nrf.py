#!/usr/bin/env python
import threading

import spidev, RPi.GPIO as GPIO, time
from lib.Nrf24 import *


class Nrf(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.pipes = [[0x00,0x01,0x03,0x07,0x00], [0x00,0x01,0x03,0x07,0x00]]
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        self.spi = spidev.SpiDev()
        self.spi.open(0, 0)
        GPIO.setup(8, GPIO.OUT)

        #self.spi.xfer2([0x20, 0x4E]) #setting config register : sender
        self.spi.xfer2([0x20, 0x3F])  # setting config register : reciever


        self.radio = NRF24(GPIO, self.spi)
        self.radio.begin(0, 25)
        self.radio.openWritingPipe(self.pipes[1])
        self.radio.openReadingPipe(0, self.pipes[1])
        self.radio.setDataRate(NRF24.BR_1MBPS)
        self.radio.setPayloadSize(32)
        self.radio.setChannel(0x01)
        self.radio.enableDynamicPayloads()
        self.radio.setAutoAck(True)
        self.radio.enableAckPayload()
        time.sleep(0.5)
        #if not work add time.sleep(0.5)
        self.radio.startListening()

    def send(self, value, id):
        self.radio.stopListening()
        self.spi.xfer2([0x20, 0x4E])  # setting config register : sender
        self.radio.write(str(value) + str(id))
        self.radio.startListening()

    def run(self):
        while True:
            try:
                pl_buffer=[]
                self.radio.read(pl_buffer, self.radio.getDynamicPayloadSize())
                s = ""
                for i in range(0, self.radio.getDynamicPayloadSize() + 1):
                    s += chr(pl_buffer[i])
                if s[0] == "@":
                    print ("Received back:")
                    print(s)
                #self.radio.flush_rx()
            except:
                time.sleep(0.1)
            time.sleep(0.01)

# while True:
#     # send a packet to receiver
#     radio.write(buf)
#     print ("Sent:"),
#     print (buf)
#     # did it return with a payload?
#     if radio.isAckPayloadAvailable():
#         pl_buffer=[]
#         radio.read(pl_buffer, radio.getDynamicPayloadSize())
#         print ("Received back:"),
#         print (pl_buffer)
#     else:
#         print ("Received: Ack only, no payload")
#     time.sleep(1)
#






# buf=[0x1D]
# buf.append(0xff)
# print(spi.xfer2(buf))
# spi.xfer2([0x24,0x4f])#setting SETUP_RETR register
# spi.xfer2([0x17,0xff]) #reading fifo_status register
# #print(spi.xfer2([0xE1])) #flush tx
# #print(radio.spidev.xfer2([0xA0, ord('1'), ord('3')]))
#
#
#
#
# def init():
#     GPIO.setmode(GPIO.BCM)
#     GPIO.setwarnings(False)
#     GPIO.setup(8, GPIO.OUT)
#
# def csnHi():
#     GPIO.output(8, GPIO.HIGH)
#
# def csnLow():
#     GPIO.output(8, GPIO.LOW)
#
# def xfer2(b):
#     l = [b]
#     return spi.xfer2(l)
#
#
# radio.setRetries(15,15)
# radio.setChannel(0x4c)
#
#
# radio.openWritingPipe(pipes[1])
# radio.openReadingPipe(1, pipes[0])
# radio.printDetails()
#
#






