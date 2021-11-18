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

#Test Inputs here
#incoming_sms = "list lockers"
#incoming_sms = "checkout"
incoming_sms = "help"
#incoming_sms = "renew jfkd help he lp chekc checkout :$#@fdah9  \n list "
#incoming_sms = "Nala"
#incoming_sms = "he lp"




#parse incoming sms
commands = []
commands.append('help')		#instructions and a list of available lockers
commands.append('checkout')	#in the form of 'checkout <lockername>'
commands.append('renew')	#target locker based on origin number


found = re.findall(r"(?=("+'|'.join(commands)+r"))", incoming_sms)
for word in found:
	print word

if len(found) > 1:
	print('too many commands!')
if len(found) == 1:
	print('found command ' + found[0] + '!')
if len(found) < 1:
	print("didn't find command!")






