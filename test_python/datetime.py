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

from module import Transmitter
from module import SMS
from little_free_locker import Locker
from little_free_locker import Lockers

#load stuff
main_lockers = Lockers()
main_lockers.load_lockers_from_user_input_txt_file("template.txt")
lenlocker = main_lockers.get_locker_obj_given_locker_name("Lenron")

phone_number = '5039895540'
main_lockers.remove_locker(lenlocker)
lenlocker.checkout_locker(phone_number)
main_lockers.add_locker(lenlocker)

if main_lockers.user_has_locker_checkedout(phone_number):
	print "locker is checkedout!"
else:
	print "locker not checkedout!"


main_lockers.save_lockers_to_json_file()




exit(0)
print "is locker checked out: " + str(locker.is_locker_checked_out())
#locker.checkout_locker(phone_number)
locker.renew_locker()
print "is locker checked out: " + str(locker.is_locker_checked_out())
main_lockers.add_locker(locker)
main_lockers.save_lockers_to_json_file()

new_lockers = Lockers()
new_lockers.load_lockers_from_user_input_txt_file("template.txt")

nlocker = new_lockers.get_locker_obj_given_locker_name("Lenron")
print "is locker checked out: " + str(nlocker.is_locker_checked_out())

nlocker.freeup_locker()

print "is nlocker checked out: " + str(nlocker.is_locker_checked_out())


#start_date = locker.start_date
#start_datetime_obj = locker.deserialize_date(start_date)

#print start_datetime_obj.strftime("%d, %b, %Y")

#check_out_day = datetime.now()

#serialized_date = locker.serialize_date(check_out_day)
#print "the serialized date is: ~" + serialized_date + "~"

#locker.start_date = serialized_date

#main_lockers.add_locker(locker)
#main_lockers.save_lockers_to_json_file()



#now = datetime.now()
#print "test if this is string: ~" + now.strftime('%d, %b.. %Y') + "~"

#delta = timedelta(days=int(locker.checkout_time_length))

#test_date = datetime(year=2009, month=3, day=3)
#print "computed test date: " + test_date.strftime('%d, %b, %Y')



#due_date = now + delta
#locker.due_date = due_date
#main_lockers.remove_locker(locker)
#main_lockers.add_locker(locker)
#main_lockers.save_lockers_to_json_file()
#new_lockers = Lockers()
#new_lockers.json_file_to_lockers_obj()
#nlocker = new_lockers.get_locker_obj_given_locker_name("Lenron")




#print "you checked out on " + now.strftime('%d, %b.. %Y') + ". your locker will expire on " + due_date.strftime('%d, %b.. %Y')

#print "now: " + now + " delta: " + delta + " dude_date: " + due_date
