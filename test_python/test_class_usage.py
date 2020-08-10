#!/usr/bin/python
#Don't create a pesky .pyc file.
import sys
sys.dont_write_bytecode = True
from module import Transmitter

tx = Transmitter()
tx.send_text('5039895540', 'testing send_text using OO structure')
