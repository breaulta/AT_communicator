#!/usr/bin/python
#Don't create a pesky .pyc file.
import sys
sys.dont_write_bytecode = True
from little_free_locker import Locker

locker_database_file = "locker_database.json"

#create a couple locker objects
locker = Locker(name = 'test1', combo = '21.14.0', address = '121 n testing ave', host_number = '5039895540', current_borrower_number = '5033803136', checkout_time_length = '14', start_date = '9/1/2020')
#serialize them
locker.save_locker_obj_to_json_file(locker_database_file)
#reload them
lkr = Locker
lkr = locker.json_file_to_locker_obj(locker_database_file)

print "locker name: " + lkr.name
print "locker address: " + lkr.address
