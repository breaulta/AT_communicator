#!/usr/bin/python
import time
from datetime import datetime, timedelta
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

	#Ensure sim/hat is set up and able to send/receive texts.
	tx.ensure_sim_card_connected_to_network("/dev/cdc-wdm0")
	#Read in any potential new texts (incoming sms).
	print "We're running get all texts now!"
	#Query sim/hat for any new texts it has received.
	new_sms_array = tx.get_all_texts()

	#If there are texts in the new_sms_array, we know we have new texts to process.
	if len(new_sms_array) > 0:
		print "We have new messages!"
		#Save any new texts from the sim card to the pi's hard drive.
		tx.append_texts_to_db_file(new_sms_array, sms_database_filename)
		#Now that we've saved them from the hard drive, we can delete from the sim card.
		tx.delete_texts_from_sim_card(new_sms_array)

		#~~~~~~~~~~~~~~~~~~~~
		#		locker.respond_to_new_texts(tx, new_sms_array)
		# not sure if we wanted to make this method or were going to do it another way.
		#~~~~~~~~~~~~~~~~~~

		#Little free locker response to new texts
		#Incoming sms should be only the name of the locker they're trying to checkout.
		for sms in new_sms_array:
			print "received sms message: ~" + sms.message + "~" #debugging
			#Cycle through lockers to see if the incomming sms matches a locker name.
			for locker in main_lockers.lockers:
				#In order for the (\b) to work we needed the r.
				#We are doing the best we can to extract the locker name from the incomming sms message.
				m = re.search(r'^\s*\b(.+)\b\s*$', sms.message)
				if m:
					#Match case-insensitively the name of the locker to the text message.
					if m.groups()[0].lower() == locker.name.lower():
#Notes for next time:
#	Calculate due_date in locker method for is_locker_checked_out method
#	Create is_locker_checked_out method
#	Create checkout_locker method
#	
						


						#Check if locker is currently checked out.

						#locker.due_date = due_date
						print "you checked out on " + now.strftime('%d, %b.. %Y') + ". your locker will expire on " + due_date.strftime('%d, %b.. %Y')

						#send combo
						message = "You've checked out locker '" + locker.name + "' until " + due_date.strftime('%d, %b.. %Y') + ". Combo: " + locker.combo
						#tx.send_text(number, message)
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
