#!/usr/bin/python
#Don't create a pesky .pyc file.
import sys
sys.dont_write_bytecode = True
from little_free_locker import Locker
from little_free_locker import Lockers

locker_database_file = "locker_database.json"

#create a couple locker objects
locker = Locker(name='testlock', combo='32.51.0', address='1000 main street', host_number='5039895540', current_borrower_number='3335554444', checkout_time_length='14', start_date='9.5.2020', renewals_possible='1', renewals_used='1')
locker2 = Locker(name='testlock2', combo='32.51.0', address='1000 main street', host_number='5039895540', current_borrower_number='3335554444', checkout_time_length='14', start_date='9.5.2020', renewals_possible='1', renewals_used='1')
#serialize them
locker.save_locker_obj_to_json_file(locker_database_file)
#reload them
#lkr = Locker
lkr = locker.json_file_to_locker_obj(locker_database_file)


lockers_obj = Lockers()
lockers_obj.add_locker(lkr)
lockers_obj.add_locker(locker2)


lockers_obj.print_lockers()
lockers_obj.save_lockers_to_json_file("lockers_output.dat")
