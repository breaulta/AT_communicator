#!/usr/bin/python
import time
from datetime import datetime, timedelta
import serial
import re
import json
import ast
import os
import logging
import sys
#Don't write a pesky .pyc file.
sys.dont_write_bytecode = True

from gsmmodem.modem import GsmModem
from little_free_locker import Locker
from little_free_locker import Lockers
from streamtologger import StreamToLogger
# For testing
from module import SMS

PORT = '/dev/ttyUSB2'
BAUDRATE = 115200
PIN = None # SIM card PIN (if any)

sms_database_filename = "sms_database.json"
new_sms_path = './incoming_sms'

# SMS stock messages
help_message = "In order to checkout a locker, text this number 'checkout <name_of_locker>'. Command words are 'help' 'renew' 'checkout'. The list of available lockers are as follows: "
error_toomany_message = "Sorry, that was too many command words. " + help_message
error_toofew_message = "Sorry, that was too few command words. " + help_message
error_generic_message= "Sorry, I did not understand that. " + help_message
checkout_message = "Congratulations! You have successfully checked out (locker.name). To open this locker, use the combination: (locker.combo) . This locker must be emptied by (locker.due_date)."
error_toomany_names = "There were too many matched lockernames in your command. You cannot checkout multiple lockers. Please reply with exactly one lockername in order to checkout that locker." + help_message
error_toofew_names = "You didn't appear to correctly input the name of the locker you wish to checkout." + help_message
no_renewals_left_msg = "Sorry, there are no renewals left for this checkout period."
locker_renewed_msg = "Your locker has been renewed."
locker_not_checked_out_msg = "No locker has been checked out with the number you're texting from."
locker_cluster_full_msg = "This locker cluster is full. The next possible opening is: "
error_one_per_tenant = "Sorry, this locker bank only allows a tenant to check out one locker at a time."

# SMS commands
commands = []
commands.append('help')     #instructions and a list of available lockers
commands.append('checkout') #in the form of 'checkout <lockername>'
commands.append('renew')    #target locker based on origin number

# send sms function that includes the log.
def send_sms(modem, number, message):
	logger = logging.getLogger('LFL_app.send_sms')
	logger.info('Sending sms with text: ' + message + ' to phone number: ' + number)
	modem.sendSms(number, message)

# Extract a single command from the input, error if there is not exactly 1 command.
def find_command(incoming_sms, origin_number):
    #find all matches of the words in commands in the string incoming_sms
    found = re.findall(r"(?=("+'|'.join(commands)+r"))", incoming_sms)
    # exactly 1 command is valid.
    if len(found) > 1:
        print(error_toomany_message)
		#modem.sendSms(error_toomany_message, origin_number)
    elif len(found) < 1:
        print(error_toofew_message)
		#modem.sendSms(error_toofew_message, origin_number)
    elif len(found) == 1:
        print('found command ' + found[0] + '!')
        command = found[0]
        return command

# Maybe delete this 
def find_lockername(incoming_sms, origin_number):
	foundnames = re.findall(r"(?=("+'|'.join(lockernames)+r"))", incoming_sms)
	if len(foundnames) > 1:
		print(error_toomany_names)
		#modem.sendSms(error_toomany_names, origin_number)
	elif len(foundnames) < 1:
		print(error_toofew_names)
		#modem.sendSms(error_toofew_names, origin_number)
	elif len(foundnames) == 1:
		lockername = foundnames[0]
		return lockername

# Callback function for modem. Converts caught SMS object into a unique file which is picked up in main.
# This is done in order to 
#def handleSms(sms_obj):
def handleSms(incoming_sms_obj):
	logger = logging.getLogger('LFL_app.handleSms')
	logger.info('Caught incoming sms from:' + incoming_sms_obj.number + ' message:' + incoming_sms_obj.text )
	# Create dir if it doesn't already exist.
	try:
		os.makedirs(new_sms_path)
	except OSError:
		if not os.path.isdir(new_sms_path):
			raise Exception('dir not created for some reason')
	#filename = new_sms_path + '/' + incoming_sms_obj.time + '_new_sms.txt'
	# use seconds since epoch as unique identifier.
	filename = new_sms_path + '/' + str(time.time()) + '_new_sms.txt'

	# If it opens, it exists => fail.
	try:
		f = open(filename)
	# Working properly.
	except IOError:
		sms_obj = SMS(phone=str(incoming_sms_obj.number), message=incoming_sms_obj.text, date=time.time())
		f = open(filename, 'w')
		sms_list = str(vars(sms_obj))
		json_sms_obj = ast.literal_eval(sms_list)
		#sms_list_str = json.dumps
		f.write(json.dumps(json_sms_obj))
		#f.write(incoming_sms_obj.number + ':' + incoming_sms_obj.text)
		f.close
	else:
		raise Exception('Generated file for incoming SMS should not already exist!')


# pull in sms data from new sms file and execute locker control logic on it.
def check_new_sms(locker_bank, modem):
	if os.path.isdir(new_sms_path):
		dirlist = os.listdir(new_sms_path)
		if not dirlist:
			print 'found no new file'
		else:
			# allows for other files in the dir to not break it.
			for filename in dirlist:
				match = re.search('\d+_new_sms.txt', filename)
				if match:
					#fil = path + '/' + dirlist[0]
					fil = new_sms_path + '/' + filename
					fd = open(fil, 'r')
					#print fd.read()
					# create SMS object and store data there
					#newSms = SMS()
					json_read_dict = json.load(fd)
					fd.close()
					os.remove(fil)
					sms = SMS(**json_read_dict)
					
					# Boomerang test
					modem.sendSms(sms.phone, sms.message)
					#print sms.index
					#parse_and_operate_sms(locker_bank, sms, modem)
				else:
					print 'found a non-matching file'
	else:
		print 'dir not created yet'


def parse_and_operate_sms(locker_bank, sms_obj, modem):
	# change after testing
	incoming_sms = sms_obj.message
	incoming_number = sms_obj.phone
	
	#command = decode_input(incoming_sms.text, incoming_sms.number)
	command = find_command(incoming_sms, incoming_number)
	if command == 'help':
		print help_message + locker_bank.list_available_lockers()
	elif command == 'renew':
		if locker_bank.user_has_locker_checkedout(incoming_number):
			#print incoming_number
			locker = locker_bank.get_locker_obj_given_locker_number(incoming_number)
			#print locker
			renewals_left = locker.get_renewals_left()
			if renewals_left < 1:
				print no_renewals_left_msg + " Your locker due date is " + locker.due_date
			else:
				locker.renew_locker()
				print "send text informing host of renewal"
				print locker_renewed_msg + " Your locker due date is " + locker.due_date + ". You have " + str(locker.get_renewals_left()) + " renewals left."
		else:
			print locker_not_checked_out_msg
	elif command == 'checkout':
		# Inform potential tenant of the earliest they could checkout a locker.
		if locker_bank.is_locker_cluster_full():
			print locker_cluster_full_msg + locker_bank.earliest_possible_release()
		else:
			lockernames = locker_bank.get_locker_list()
			foundnames = re.findall(r"(?=("+'|'.join(lockernames)+r"))", incoming_sms)
			if len(foundnames) > 1:
				print(error_toomany_names)
			elif len(foundnames) < 1:
				print(error_toofew_names)
			elif len(foundnames) == 1:
#               print('found lockername ' + foundnames[0] + '!') # Debug
				lockername = foundnames[0]
				print 'try to checkout: ' + lockername  # Debug
				# try to checkout, give list of available otherwise
				result = locker_bank.checkout_locker(incoming_number, lockername)
				if result == 1:
					locker_obj = locker_bank.get_locker_obj_given_locker_name(lockername)
					print "You have successfully checked out locker '" + lockername + "'. The combo is: " + locker_obj.combo + ". The current due date is: " + locker_obj.due_date + ". You may renew " + str(locker_obj.get_renewals_left()) + " times."
				elif result == 'duplicate number':
					print "There is already a locker checked out under this number!"
				elif result == 'checked out':
					print "The locker " + lockername + " has already been checked out! Other available lockers: " + locker_bank.list_available_lockers()
				##else:
					# There is at least one locker or
					# locker_bank.is_locker_cluster_full would prevent getting here.
					#print 'no checkout... BUT! ' + locker_bank.list_available_lockers()
				##	print "The locker " + lockername + " could not be checked out at this time. However, other lockers are available: " + locker_bank.list_available_lockers()


def setUpLogging():
	#logger = logging.getLogger()
	#logger.addHandler('LFL_app')
	#logger.addHandler('gsmmodem')
	
	# LFL_app is the identifier.
	logger = logging.getLogger('LFL_app')
	logger.setLevel(logging.DEBUG)

	modem_logger = logging.getLogger('gsmmodem')
	

	# create file handler which logs even debug messages
	fh = logging.FileHandler('locker.log')
	# Send everything to logfile.
	fh.setLevel(logging.DEBUG)
	# create console handler with a higher log level
	ch = logging.StreamHandler()
	# Also show everything in stdout. 
	ch.setLevel(logging.DEBUG) 
	#ch.setLevel(logging.ERROR)
	# create formatter and add it to the handlers
	formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
	fh.setFormatter(formatter)
	ch.setFormatter(formatter)
	# add the handlers to the logger
	logger.addHandler(fh)
	logger.addHandler(ch)

	modem_logger.addHandler(fh)
	modem_logger.addHandler(ch)

	# Send everything from stdout and stderr to the logfile.
	stdout_logger = logging.getLogger('LFL_app.stdout')
	sl = StreamToLogger(stdout_logger, logging.INFO)
	sys.stdout = sl
	stderr_logger = logging.getLogger('LFL_app.stderr')
	sl = StreamToLogger(stderr_logger, logging.ERROR)
	sys.stderr = sl


def timing_renewal_handler(main_lockers, server_start_time, modem):
	logger = logging.getLogger('LFL_app.timing_renewal_handler')
	now = datetime.now() #keep calculating
	# log message stating the program status every hour. uptime, number of lockers and due date, 
	uptime_calc = now - server_start_time
	uptime_seconds = int(uptime_calc.total_seconds())
	uptime_hours = uptime_seconds / 3600
	#if uptime_seconds % 3 == 0:
	if uptime_seconds % 3600 == 0:
		logger.info('Server uptime: ' + str(uptime_hours) + ' hours. ' + 'Uptime seconds: ' + str(uptime_seconds))
	bank = main_lockers.get_locker_list()
	for lockername in bank:
		locker_obj = main_lockers.get_locker_obj_given_locker_name( lockername )
		#if hasattr(locker_obj, 'due_date'):
		if locker_obj.is_locker_checked_out():
			duedate = locker_obj.deserialize_date()
			diff = duedate - now
			seconds = diff.total_seconds()
			hours = seconds / 3600
			print hours #debug
			#renew hours left check
			if hours <= 48 and locker_obj.twodayflag == 1:
				locker_obj.twodayflag = 0
				print "48 hour message for: "  + lockername
			if hours <= 24 and locker_obj.onedayflag == 1:
				locker_obj.onedayflag = 0
				print "24 hour message for: " + locker_obj.name
				#continue
			if hours <= 0 and locker_obj.is_locker_checked_out():
				# Close tenancy of current locker.
				#Notify host and tenant of expiration.
				main_lockers.freeup_locker(lockername)
				print 'the locker: ' + lockername + ' has been closed!'
			else:
				print 'the locker: ' + lockername + ' is checked out and not due.'


def main():
	#Ensure that we're running as root.
	if not os.geteuid()==0:
		raise Exception("Must run as root!")
	# For uptime, hourly calculation
	start_time = datetime.now()
	setUpLogging()
	main_lockers = Lockers()
	# Load unique locker setup from template file curated for host input.
	main_lockers.load_lockers_from_user_input_txt_file("template.txt")

	#Initialize Modem, set to call handleSms() when a text is received.
	modem = GsmModem(PORT, BAUDRATE, smsReceivedCallbackFunc=handleSms)
	#Sets modem to PDU mode, not sure why they do this in the example text...
	modem.smsTextMode = False
	modem.connect(PIN)
	# will need to pass modem into anything that's sending texts

	# Spawn renewal messages and save state.
	while 1:
		# Check for new messages and operate on them.
		check_new_sms(main_lockers, modem)
		# Check if a renewal message needs to be spawned and handle timing events.
		timing_renewal_handler(main_lockers, start_time, modem)
		# Back up data/save current state.
		main_lockers.save_lockers_to_json_file()
		time.sleep(2)



if __name__ == '__main__':
    main()


#Need timer to track checkout period for each locker.
#Current idea is to calculate and save the epoch date to each locker object that is checked out.
#	In a non-blocking loop check each locker for end date epoch (datetime) entries
#		Check the difference between now and the end date <= 48 hours (or whatever)
#		Set has_48hours_elapsed flag or something so it doesn't keep spamming messages.
#		Wait (sleep?) in a non-blocking manner.


#CODE TO WRITE: locker due date reminder text
#Two lockers of the same name check?

#MORE CODE:
#Did we ever check on phone numbers with hyphens for texting?

# Periodically save lockers to json file in case of crash
#main_lockers.save_lockers_to_json_file()

#Called when pgsmm detects an incoming text
#sms attributes: number, text, smsc, time
#*TEST NEEDED* to reveal the contents of the sms array
#probably others; print out the contents of the sms array to find out
#*TEST NEEDED* Check if old functionality works with sms call back system below


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

