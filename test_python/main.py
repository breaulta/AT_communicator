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
	#Read in any potential new texts (incoming sms).
	new_sms_array = tx.get_all_texts()

	#Check if we have new texts...
	if len(new_sms_array) > 0:
		tx.append_texts_to_db_file(new_sms_array, sms_database_filename)
		tx.delete_texts_from_sim_card(new_sms_array)
		#Little free locker response to new texts
		#locker.respond_to_new_texts(tx, new_sms_array)


#check for incoming sms messages

#act on that sms message smartly

#save the sms

#perform some logic
