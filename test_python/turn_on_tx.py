#!/usr/bin/python
#Don't create a pesky .pyc file.
import sys
sys.dont_write_bytecode = True

from module import Transmitter

tx = Transmitter(port = '/dev/ttyUSB2')

tx.ensure_sim_card_connected_to_network("/dev/cdc-wdm0")
