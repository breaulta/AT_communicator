#!/usr/bin/python
#Don't create a pesky .pyc file.
import sys
sys.dont_write_bytecode = True
from little_free_locker import Locker
from little_free_locker import Lockers

locker_database_file = "locker_database.json"

#create a couple locker objects
locker = Locker(name='testlock', combo='32.51.0', address='1000 main street', host_number='5039895540', current_borrower_number='3335554444', checkout_time_length='14', start_date='9.5.2020', renewals_possible='1', renewals_used='1')
#serialize them
locker.save_locker_obj_to_json_file(locker_database_file)
#reload them
#lkr = Locker
lkr = locker.json_file_to_locker_obj(locker_database_file)
#print "locker name: " + locker.name
print "locker name: " + lkr.name
locker1 = locker.name
locker2 = lkr.name

print "will the real locker stand up: " + locker1

#Python treating locker1 and locker2 here as strings, not interpolating them as variables as would be expected in Perl.
args = {
	locker.name: locker,
	lkr.name: lkr
}
#big_lockers = Lockers(locker1 = locker, locker2 = lkr)
big_lockers = Lockers(args)
#big_lockers = Lockers()
