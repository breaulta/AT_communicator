#!/usr/bin/python
import time
import serial
import re
import json
import os
#Don't write a pesky .pyc file.
import sys
sys.dont_write_bytecode = True

from module import Transmitter
from module import SMS
from little_free_locker import Locker
from little_free_locker import Lockers

#load stuff
main_lockers = Lockers()
main_lockers.load_lockers_from_user_input_txt_file("template.txt")
#maybe load sms messages??? can't think of a reason why right now....

sms_database_filename = "sms_database.json"
tx = Transmitter(port = '/dev/ttyUSB2')

#infinite loop
while(1):
	
	tx.ensure_sim_card_connected_to_network("/dev/cdc-wdm0")
	#Read in any potential new texts (incoming sms).
	print "We're running get all texts now!"
	new_sms_array = tx.get_all_texts()

	#Check if we have new texts...
	if len(new_sms_array) > 0:
		print "We have new messages!"
		tx.append_texts_to_db_file(new_sms_array, sms_database_filename)
		tx.delete_texts_from_sim_card(new_sms_array)
		#Little free locker response to new texts
		#locker.respond_to_new_texts(tx, new_sms_array)
		#Incoming sms should be only the name of the locker they're trying to checkout.
		for sms in new_sms_array:
			print "received sms message: ~" + sms.message + "~"
			for locker in main_lockers.lockers:
				#maybe regex here to clean up incoming sms.
				m = re.search(r'^\s*\b(.+)\b\s*$', sms.message)
				if m:
					#If we matched the 'name' case-insensitively at the beginning of locker parameters.
					if m.groups()[0].lower() == locker.name.lower():
						#print "group matched: ~" + m.groups()[0] + "~"
						#set timer based on checkout time. probably use 'datetime' package
						#send combo
						#locker.send_text(number, message)
						message = "You've checked out locker '" + locker.name + "' until " + date ". Combo: " + locker.combo
						print "sending text. number:~" + sms.phone + "~ message:~" + message + "~"
						#record/notify that this locker has been checked out.
					else:
						print "group didn't match for some reason"
				else:
					print "text received but not caught by regex :("
	time.sleep(15)


#check for incoming sms messages

#act on that sms message smartly

#save the sms

#perform some logic
