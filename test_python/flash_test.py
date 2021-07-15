#!/usr/bin/python
# -*- coding: utf-8 -*-
import time
import serial       #Works on Len's pi. Looks like it's a tough, depreciated package otherwise.
import re
import json
import os

#Don't write a pesky .pyc file.
import sys
sys.dont_write_bytecode = True

from gsmmodem.modem import GsmModem

PORT = '/dev/ttyUSB2'
BAUDRATE = 115200

modem = GsmModem(PORT, BAUDRATE)
modem.connect()
print('connected')
smsObj = modem.sendSms('5039895540', 'flash me baby', sendFlash=True)
print smsObj
