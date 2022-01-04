#!/usr/bin/python
import time
from datetime import datetime, timedelta
import serial
import re
import json
import os
import logging
import sys
#Don't write a pesky .pyc file.
sys.dont_write_bytecode = True

from gsmmodem.modem import GsmModem
from little_free_locker import Locker
from little_free_locker import Lockers
from streamtologger import StreamToLogger

PORT = '/dev/ttyUSB2'
BAUDRATE = 115200
PIN = None # SIM card PIN (if any)

sms_database_filename = "sms_database.json"

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

# To be deleted once integration testing is done:
#Test Inputs here
#incoming_sms = "list lockers"
#incoming_sms = "checkout"
incoming_sms = "checkout Nala"
#incoming_sms = "help"
#incoming_sms = "renew jfkd help he lp chekc checkout :$#@fdah9  \n list "
#incoming_sms = "Nala"
#incoming_sms = "he lp"
#incoming_sms = "checkout Nala" # Test checkout bloc
#incoming_sms = "renew"

#incoming_number = "fake number"
incoming_number = "5039895540"

# SMS commands
commands = []
commands.append('help')     #instructions and a list of available lockers
commands.append('checkout') #in the form of 'checkout <lockername>'
commands.append('renew')    #target locker based on origin number

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

def handleSms(sms_obj):
	# Create text file.
	# Write data to text file.
	# Notify 


def handleSms(incoming_sms):
	#command = decode_input(incoming_sms.text, incoming_sms.number)
	command = decode_input(incoming_sms, incoming_number)
	if command == 'help':
        print help_message + locker_bank.list_available_lockers()
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
                print locker_renewed_msg + " Your locker due date is " + locker.due_date + ". You have " + str(renewals_left) + " renewwals left."
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
                if locker_bank.checkout_locker(sms_origin_number, lockername):
                    locker_obj = locker_bank.get_locker_obj_given_locker_name(lockername)
                    print "You have successfully checked out locker '" + lockername + "'. The combo is: " + locker_obj.combo + ". The ccurrent due date is: " + locker_obj.due_date + ". You may renew " + str(locker_obj.get_renewals_left()) + " times."
                else:
                    # There is at least one locker or
                    # locker_bank.is_locker_cluster_full would prevent getting here.
                    #print 'no checkout... BUT! ' + locker_bank.list_available_lockers()
                    print "The locker " + lockername + " could not be checked out at this time. However, other lockers are available: " + locker_bank.list_available_lockers()


def setUpLogging():
	# LFL_app is the identifier.
	logger = logging.getLogger('LFL_app')
	logger.setLevel(logging.DEBUG)
	# create file handler which logs even debug messages
	fh = logging.FileHandler('locker.log')
	# Send everything to logfile.
	fh.setLevel(logging.DEBUG)
	# create console handler with a higher log level
	ch = logging.StreamHandler()
	# Show everything in stdout. 
	ch.setLevel(logging.DEBUG) 
	#ch.setLevel(logging.ERROR)
	# create formatter and add it to the handlers
	formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
	fh.setFormatter(formatter)
	ch.setFormatter(formatter)
	# add the handlers to the logger
	logger.addHandler(fh)
	logger.addHandler(ch)

	# Send everything from stdout and stderr to the logfile.
	stdout_logger = logging.getLogger('LFL_app')
	sl = StreamToLogger(stdout_logger, logging.INFO)
	sys.stdout = sl
	stderr_logger = logging.getLogger('LFL_app')
	sl = StreamToLogger(stderr_logger, logging.ERROR)
	sys.stderr = sl


def main():
	#Ensure that we're running as root.
	if not os.geteuid()==0:
		raise Exception("Must run as root!")

	setUpLogging()
	main_lockers = Lockers()
	# Load unique locker setup from template file curated for host input.
	main_lockers.load_lockers_from_user_input_txt_file("template.txt")

	#Initialize Modem, set to call handleSms() when a text is received.
	#modem = GsmModem(PORT, BAUDRATE, smsReceivedCallbackFunc=handleSms)
	#Sets modem to PDU mode, not sure why they do this in the example text...
	#modem.smsTextMode = False
	#modem.connect(PIN)

	# Spawn renewal messages and constantly save state.
	while 1:
		# Check if a renewal message needs to be spawned.
		# Back up data/save current state.
		# Check for new messages.


		now = datetime.now() #keep calculating
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
				if hours <= 24 and locker_obj.onedayflag == 1:
					locker_obj.onedayflag = 0
					print "24 hour message"
					continue
				elif hours <= 48 and locker_obj.twodayflag == 1:
					locker_obj.twodayflag = 0
					print "48 hour message"
				elif hours <= 0 and locker_obj.is_locker_checked_out():
					# Close tenancy of current locker.
					#Notify host of expiration.
					locker_obj.freeup_locker()
				else:
					print "not due"
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

