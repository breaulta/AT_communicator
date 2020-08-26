#!/usr/bin/python


#note for next time:
#	add turn sim card on functionality to class
#	and verifiy that it's on
#	add periodic new sms functionality to class
#	could be done by spawning separate process
	#separate script that reboots our SIM script when pi power cycles


#Don't create a pesky .pyc file.
import sys
sys.dont_write_bytecode = True

from module import Transmitter

tx = Transmitter(port = '/dev/ttyUSB2')

tx.ensure_sim_card_connected_to_network("/dev/cdc-wdm0")
