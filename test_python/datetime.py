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
locker = main_lockers.get_locker_obj_given_locker_name("Lenron")


now = datetime.now()
print "test if this is string: ~" + now.strftime('%d, %b.. %Y') + "~"

delta = timedelta(days=int(locker.checkout_time_length))

due_date = now + delta
locker.due_date = due_date


print "you checked out on " + now.strftime('%d, %b.. %Y') + ". your locker will expire on " + due_date.strftime('%d, %b.. %Y')

#print "now: " + now + " delta: " + delta + " dude_date: " + due_date
