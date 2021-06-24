#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function

#Don't write a pesky .pyc file.
import sys
sys.dont_write_bytecode = True
#sys.path.append('/path/to/application/app/folder')

from gsmmodem.modem import GsmModem
#from gsmtermlib.terminal import RawTerm

PORT = '/dev/ttyUSB2'
BAUDRATE = 9600

print('start main...')
modem = GsmModem(PORT, BAUDRATE)
modem.connect()
print('before')
print(modem.write('AT'))
print('after')
