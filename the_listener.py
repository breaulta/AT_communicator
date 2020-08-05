#!/usr/bin/python
import time
import serial

# configure the serial connections (the parameters differs on the device you are connecting to)
ser = serial.Serial(
    port='/dev/ttyUSB2',
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_TWO,
    bytesize=serial.EIGHTBITS,
)

ser.isOpen()


while 1 :
    #time.sleep(.5)
    command = ser.read_until()
    print str(command)
