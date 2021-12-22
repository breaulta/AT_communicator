#!/usr/bin/python
import time
from datetime import datetime, timedelta
import json
import os
#Don't write a pesky .pyc file.
import sys
sys.dont_write_bytecode = True

from little_free_locker import Locker
from little_free_locker import Lockers

main_lockers = Lockers() #init
main_lockers.load_lockers_from_user_input_txt_file("template.txt") #adds lockers from user input file


"""
lst = locker_bank.get_locker_list()
for locker in lst:
	print locker
later = datetime(2021, 11, 20)
now = datetime.now()
#diff = later - now #diff is now a timedelta
#seconds = diff.total_seconds()
#hours = int(seconds) / 3600.0
#print hours

obj = locker_bank.get_locker_obj_given_locker_name('Nala')
obj.checkout_locker("5039895540")
date = obj.deserialize_date( obj.due_date )
diff = date - now
seconds = diff.total_seconds()
hours = seconds / 3600
print hours
if hours <= 48:
	print "due"
else:
	print "not due"
"""

#obj.checkout_locker("5039895540")
main_lockers.checkout_locker('5039895540', 'Nala')
obj = main_lockers.get_locker_obj_given_locker_name('Nala')
obj.due_date = '11/19/2021'

#Spawn renewal messages
while 1:
	now = datetime.now() #keep calculating
	bank = main_lockers.get_locker_list() #from main.pl initialization
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


#Need timer to track checkout period for each locker.
#Current idea is to calculate and save the epoch date to each locker object that is checked out.
#   In a non-blocking loop check each locker for end date epoch (datetime) entries
#       Check the difference between now and the end date <= 48 hours (or whatever)
#       Set has_48hours_elapsed flag or something so it doesn't keep spamming messages.
#       Wait (sleep?) in a non-blocking manner.
