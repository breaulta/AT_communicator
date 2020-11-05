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

#Import classes to deal with SIM card and SMS objects
from module import Transmitter
from module import SMS

sms_database_filename = "sms_database.json"

tx = Transmitter(port = '/dev/ttyUSB2', qmi_path = '/dev/cdc-wdm0')
tx.send_text('5039895540', 'sudo at test')
exit(0)
#Get new sms messages from SIM card in array.
new_sms_array = tx.get_all_texts()

#Check if we have new texts...
if len(new_sms_array) > 0:
	tx.append_texts_to_db_file(new_sms_array, sms_database_filename)
	tx.delete_texts_from_sim_card(new_sms_array)
	#Little free locker response to new texts
#	locker.respond_to_new_texts(tx, new_sms_array)

