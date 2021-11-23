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

from little_free_locker import Locker
from little_free_locker import Lockers

locker_bank = Lockers()
locker_bank.load_lockers_from_user_input_txt_file("template.txt")

help_message = "In order to checkout a locker, text this number (locker_bank_number) 'checkout <name_of_locker>'. This list of lockers are as follows: (names_of_lockers). Command words are 'help' 'renew' 'checkout'."
error_toomany_message = "Sorry, that was too many command words. Command words are 'help' 'renew' 'checkout. " + help_message
error_toofew_message = "Sorry, that was too few command words. Command words are 'help' 'renew' 'checkout. " + help_message
error_generic_message= "Sorry, I did not understand that. " + help_message
renew_message = "You have renewed the locker.\nThe checkout period for this locker may be renewed up to (locker.total_renewals_possible) more times."
checkout_message = "Congratulations! You have successfully checked out (locker.name). To open this locker, use the combination: (locker.combo) . This locker must be emptied by (locker.due_date)."
error_toomany_names = "There were too many matched lockernames in your command. You cannot checkout multiple lockers. Please reply with exactly one lockername in order to checkout that locker." + help_message
error_toofew_names = "You didn't appear to correctly input the name of the locker you wish to checkout." + help_message


#Test Inputs here
#incoming_sms = "list lockers"
#incoming_sms = "checkout"
incoming_sms = "checkout Nala"
#incoming_sms = "help"
#incoming_sms = "renew jfkd help he lp chekc checkout :$#@fdah9  \n list "
#incoming_sms = "Nala"
#incoming_sms = "he lp"


#parse incoming sms
commands = []
commands.append('help')		#instructions and a list of available lockers
commands.append('checkout')	#in the form of 'checkout <lockername>'
commands.append('renew')	#target locker based on origin number

found = re.findall(r"(?=("+'|'.join(commands)+r"))", incoming_sms)
#debugging
for word in found:
	print word

#only 1 command is valid
if len(found) > 1:
	print(error_toomany_message)
elif len(found) < 1:
	print(error_toofew_message)
elif len(found) == 1:
	print('found command ' + found[0] + '!')
	command = found[0]
	print command
	if command == 'help':
		print help_message
	elif command == 'renew':
		print renew_message
		#do some renew logic
		print "debug/log: do some renew logic, check for renewals, etc."
	elif command == 'checkout':
		#print checkout_message
		print "debug/log: do some checkout logic, checkout the locker, set timers, etc."
		lockernames = locker_bank.get_locker_list()
		foundnames = re.findall(r"(?=("+'|'.join(lockernames)+r"))", incoming_sms)
		for name in foundnames:
			print name
		if len(foundnames) > 1:
			print(error_toomany_names)
		elif len(foundnames) < 1:
			print(error_toofew_names)
		elif len(foundnames) == 1:
			print('found lockername ' + foundnames[0] + '!')
			print "debug/log: checkout the locker."







