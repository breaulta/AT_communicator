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

from gsmmodem.modem import GsmModem
#Probably not necessary anymore
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

#CODE TO WRITE: locker due date reminder text
#Two lockers of the same name check?

#MORE CODE:
#Did we ever check on phone numbers with hyphens for texting?

#########################################################
# New code to implement python-gsmmodem.
# Working without access to pi for testing: mark things that need unit testing with *TEST NEEDED*
#########################################################

#Initialize Modem, set to call handleSms() when a text is received.
modem = GsmModem(PORT, BAUDRATE, smsReceivedCallbackFunc=handleSms)
#Sets modem to PDU mode, not sure why they do this in the example text...
modem.smsTextMode = False
modem.connect()
#*TEST NEEDED*

#Called when pgsmm detects an incoming text
#sms attributes: number, text, smsc, time
#*TEST NEEDED* to reveal the contents of the sms array
#probably others; print out the contents of the sms array to find out
#*TEST NEEDED* Check if old functionality works with sms call back system below
def handleSms(incoming_sms):
	print "received sms message: ~" + sms.message + "~" #debugging
	for locker in main_lockers.lockers:
		#In order for the (\b) to work we needed the r.
		#Extract the text content from the incomming sms message.
		#
		m = re.search(r'^\s*\b(.+)\b\s*$', sms.message)
		if m:
			print "we just matched the regex " + locker.name + " : " + m.groups()[0]
			user_text_input = m.groups()[0]
			#Does the user input match the name of a locker to be checked out.
			#Match case-insensitively the name of the locker to the text message.
			if user_text_input.lower() == locker.name.lower():
				print "our name match: " + user_text_input + " " + locker.name
				#Check if the user has any other lockers checked out in this cluster.
				if main_lockers.user_has_locker_checkedout(sms.phone):
					#block them from checking out
					message = "You already have a locker checked out. This locker cluster does not allow multiple lockers to be checked out by the same number."
					tx.send_text(sms.phone, message)
					tx.send_text_to_host(locker.host_number, sms.phone, message)
				#User is good to check this locker out, so checkout the locker.
				else:
					print "we're trying to check out the locker"
					main_lockers.remove_locker(locker)
					locker.checkout_locker(sms.phone)
					main_lockers.add_locker(locker)
					main_lockers.save_lockers_to_json_file()
					message = "Congratulations! You have successfully checked out " + locker.name + ". To open this locker, use the combination: " + locker.combo + ". This locker must be emptied by " + locker.due_date + "."
					#If renewals are possible, let user know.
					if locker.total_renewals_possible > 0:
						message = message + "\n\nThe checkout period for this locker may be renewed up to " + locker.total_renewals_possible + "times."
					message = "a simple message"
					print "We're planning on sending the message: ~" + message + "~"
					tx.send_text(sms.phone, message)
					tx.send_text_to_host(locker.host_number, sms.phone, message)
					print "We've hopefully just sent that message"
		else:
			print "Text message didn't have any content? See for yourself: ~" + sms.message + "~"
	



#Need timer to track checkout period for each locker.
#Current idea is to calculate and save the epoch date to each locker object that is checked out.
#	In a non-blocking loop check each locker for end date epoch (datetime) entries
#		Check the difference between now and the end date <= 48 hours (or whatever)
#		Set has_48hours_elapsed flag or something so it doesn't keep spamming messages.
#		Wait (sleep?) in a non-blocking manner.




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

