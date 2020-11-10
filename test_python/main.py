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

#Ensure that we're running as root.
if not os.geteuid()==0:
	raise Exception("Must run as root!")

from module import Transmitter
from module import SMS
from little_free_locker import Locker
from little_free_locker import Lockers

#load stuff
main_lockers = Lockers()
main_lockers.load_lockers_from_user_input_txt_file("template.txt")
#maybe load sms messages??? can't think of a reason why right now....

sms_database_filename = "sms_database.json"
tx = Transmitter(port = '/dev/ttyUSB2', qmi_path = '/dev/cdc-wdm0')

#FIX FOR PROBLEM: TURN OFFLINE, RESET, TURN BACK ONLINE QMI DEVICE
#FIRST LINE OF DEFENSE RATHER THAN RAISING EXCEPTION
#SPACE OUT AT CALLS TO ENSURE THERE'S NEEDED SPACE

#infinite loop
while(1):
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
		for sms in new_sms_array:
			print "received sms message: ~" + sms.message + "~" #debugging
			#Cycle through lockers to see if the incomming sms matches a locker name.
			for locker in main_lockers.lockers:
				#In order for the (\b) to work we needed the r.
				#Extract the text content from the incomming sms message.
				m = re.search(r'^\s*\b(.+)\b\s*$', sms.message)
				if m:
					user_text_input = m.groups()[0]
					#Does the user input match the name of a locker to be checked out.
					#Match case-insensitively the name of the locker to the text message.
					if user_text_input.lower() == locker.name.lower():
						#Check if the user has any other lockers checked out in this cluster.
						if main_lockers.user_has_locker_checkedout(sms.phone):
							#block them from checking out
							message = "You already have a locker checked out. This locker cluster does not allow multiple lockers to be checked out by the same number."
							tx.send_text(sms.phone, message)
							tx.send_text_to_host(locker.host_number, sms.phone, message)
						else:
							print "you're good to check out"
				else:
					print "Text message didn't have any content? See for yourself: ~" + sms.message + "~"
	time.sleep(15)


#check for incoming sms messages

#act on that sms message smartly

#save the sms

#perform some logic


#check out is ok
							
#Notes for next time:
#Check-out locker
#Send text to checker-outer that locker is checked out and give them combo, and let them know the due date.
#Send text to locker owner, notifiying them of the same.

#For additional help, add yes/no to template file for help with locker:
#Have option to text owner number (please contact 503-xxx-xxxx for any additional help)

#For renewals:
#3 days before: notify them of due date and that you have x renewals, text RENEW to renew (if they have multiple lockers checked out, renew them both).
#If 0 renewals, let them know that stuff must be removed from locker by the specified due date.

#Due date reminder:
#Even if no renewals possible, remind them 48, and 24 hours before that locker needs to be cleared.
#Then, on due date, let them know that any items remaining in the locker may be forfeited if not removed today.

#Check to see if any lockers have been checked out, if they have.

#Text any discrepancies/errors to the user.

#Check if locker is currently checked out.


#send combo
#message = "You've checked out locker '" + locker.name + "' until " + locker.due_date + ". The combo to the locker is: " + locker.combo
#tx.send_text(number, message)
#print "sending text. number:~" + sms.phone + "~ message:~" + message + "~"
#record/notify that this locker has been checked out.

