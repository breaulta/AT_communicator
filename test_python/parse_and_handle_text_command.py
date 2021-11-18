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
incoming_sms = "list lockers"
incoming_sms = "checkout"
incoming_sms = "help"
incoming_sms = "renew"
incoming_sms = "Nala"
incoming_sms = "he lp"




#parse incoming sms
commands = []
commands.append('help')		#instructions and a list of available lockers
commands.append('checkout')	#in the form of 'checkout <lockername>'
commands.append('renew')	#target locker based on origin number


for command in commands:



