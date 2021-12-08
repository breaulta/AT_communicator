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
checkout_message = "Congratulations! You have successfully checked out (locker.name). To open this locker, use the combination: (locker.combo) . This locker must be emptied by (locker.due_date)."
error_toomany_names = "There were too many matched lockernames in your command. You cannot checkout multiple lockers. Please reply with exactly one lockername in order to checkout that locker." + help_message
error_toofew_names = "You didn't appear to correctly input the name of the locker you wish to checkout." + help_message
no_renewals_left_msg = "Sorry, there are no renewals left for this checkout period."
locker_renewed_msg = "Your locker has been renewed."
locker_not_checked_out_msg = "No locker has been checked out with the number you're texting from."
locker_cluster_full_msg = "This locker cluster is full. The next possible opening is: "

#Test Inputs here
#incoming_sms = "list lockers"
#incoming_sms = "checkout"
#incoming_sms = "checkout Nala"
#incoming_sms = "help"
#incoming_sms = "renew jfkd help he lp chekc checkout :$#@fdah9  \n list "
#incoming_sms = "Nala"
#incoming_sms = "he lp"
incoming_sms = "checkout Nala"	# Test checkout bloc

incoming_number = "53"
#locker = locker_bank.get_locker_obj_given_locker_name("Nala")
#print locker.due_date + 'something'
#locker._checkout_locker(incoming_number)
locker_bank.checkout_locker('fake number', 'Nala')
#locker.due_date = '12/9/2021'
#print locker.tenant_number
#lockerx = locker_bank.get_locker_obj_given_locker_number("53")
#print lockerx.tenant_number

#lockery = locker_bank.get_locker_obj_given_locker_name("3rd")
#lockery._checkout_locker('555-555-5555')	# Shouldn't be able to checkout with same number!
#locker_bank.checkout_locker('555-555-5555', '3rd')
#lockery.due_date = '12/18/2021'
#lockerz = locker_bank.get_locker_obj_given_locker_name("Lenron")
#lockerz._checkout_locker('555-555-5555')
if locker_bank.checkout_locker('555-555-5555', 'Lenron'):
	print 'checkedout'
else:
	print 'no checkout'
#lockerz.due_date = '12/8/2021'
print locker_bank.earliest_possible_release()

print locker_bank.list_available_lockers()


#parse incoming sms
commands = []
commands.append('help')		#instructions and a list of available lockers
commands.append('checkout')	#in the form of 'checkout <lockername>'
commands.append('renew')	#target locker based on origin number

#find all matches of the words in commands in the string incoming_sms
found = re.findall(r"(?=("+'|'.join(commands)+r"))", incoming_sms)
#debugging
for word in found:
	print word

sms_origin_number = '192.168.1.1'
# only 1 command is valid
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
		if locker_bank.user_has_locker_checkedout(incoming_number):
			print incoming_number
			locker = locker_bank.get_locker_obj_given_locker_number(incoming_number)
			print locker
			renewals_left = locker.get_renewals_left()
			if renewals_left < 1:
				print no_renewals_left_msg + " Your locker due date is " + locker.due_date
			else:
				locker.renew_locker
				print "send text informing host of renewal"
				print locker_renewed_msg + " Your locker due date is " + locker.due_date + ". You have " + str(renewals_left) + " renewals left."
		else:
			print locker_not_checked_out_msg
	elif command == 'checkout':
		# Inform potential tenant of the earliest they could checkout a locker.
		if locker_bank.is_locker_cluster_full():
			print locker_cluster_full_msg + locker_bank.earliest_possible_release()
		else:
			lockernames = locker_bank.get_locker_list()
			foundnames = re.findall(r"(?=("+'|'.join(lockernames)+r"))", incoming_sms)
			for name in foundnames:	#Debug
				print name
			if len(foundnames) > 1:
				print(error_toomany_names)
			elif len(foundnames) < 1:
				print(error_toofew_names)
			elif len(foundnames) == 1:
				print('found lockername ' + foundnames[0] + '!') # Debug
				lockername = foundnames[0]
				print 'try to checkout: ' + lockername	# Debug
				# try to checkout, give list of available otherwise
				if locker_bank.checkout_locker(sms_origin_number, lockername):
					print 'checkedout'
				else:
					# There is at least one locker or
					# locker_bank.is_locker_cluster_full would prevent getting here.
					print 'no checkout... BUT! ' + locker_bank.list_available_lockers()







