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

help_message = "In order to checkout a locker, text this number 'checkout <name_of_locker>'. Command words are 'help' 'renew' 'checkout'. The list of available lockers are as follows: "
error_toomany_message = "Sorry, that was too many command words. " + help_message
error_toofew_message = "Sorry, that was too few command words. " + help_message

commands = []
commands.append('help')     #instructions and a list of available lockers
commands.append('checkout') #in the form of 'checkout <lockername>'
commands.append('renew')    #target locker based on origin number


#incoming_sms = "renew jfkd help he lp chekc checkout :$#@fdah9  \n list "
incoming_sms = "checkout Nala"
origin_number = '5039895540'




def find_command(incoming_sms, origin_number):
	#find all matches of the words in commands in the string incoming_sms
	found = re.findall(r"(?=("+'|'.join(commands)+r"))", incoming_sms)
	# exactly 1 command is valid.
	if len(found) > 1:
		print(error_toomany_message)
	elif len(found) < 1:
		print(error_toofew_message)
	elif len(found) == 1:
		print('found command ' + found[0] + '!')
		command = found[0]
		return command




print find_command(incoming_sms, origin_number)
