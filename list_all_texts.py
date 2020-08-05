#!/usr/bin/python
import time
import serial

# configure the serial connections (the parameters differs on the device you are connecting to)
ser = serial.Serial(
    port='/dev/ttyUSB2',
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_TWO,
    bytesize=serial.EIGHTBITS
)

ser.isOpen()
ser.write('AT+CMGL="REC READ"' + "\r\n")
time.sleep(1)
out = ''
while ser.inWaiting() > 0:
    out += ser.read(1)
if out != '':
    print ">>>" + out

