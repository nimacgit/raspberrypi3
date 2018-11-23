#!/usr/bin/env python


import spidev, time
from nrf24 import NRF24
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)








pipes = [[0xe7, 0xe7, 0xe7, 0xe7, 0xe7], [0xc2, 0xc2, 0xc2, 0xc2, 0xc2]]

radio = NRF24(GPIO, spidev.SpiDev())
radio.begin(0, 17)
time.sleep(1)
radio.setRetries(15,15)
#radio.setPayloadSize(33)
radio.setChannel(0x4c)

radio.setDataRate(NRF24.BR_250KBPS)
radio.setPALevel(NRF24.PA_LOW)
radio.setAutoAck(True)

'''
radio.enableDynamicPayloads()
radio.enableAckPayload()

'''
radio.openWritingPipe(pipes[1])
radio.openReadingPipe(1, pipes[0])
radio.printDetails()

while True:
    buf = "11"
    # send a packet to receiver
    radio.write(buf)
    print ("Sent:"),
    print (buf)
    # did it return with a payload?
    if radio.isAckPayloadAvailable():
        pl_buffer=[]
        radio.read(pl_buffer, radio.getDynamicPayloadSize())
        print ("Received back:"),
        print (pl_buffer)
    else:
        print ("Received: Ack only, no payload")
    time.sleep(1)



