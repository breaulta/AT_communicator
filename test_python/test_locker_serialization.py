#!/usr/bin/python
#Don't create a pesky .pyc file.
import re
import sys
sys.dont_write_bytecode = True
from little_free_locker import Locker
from little_free_locker import Lockers

locker_database_file = "locker_database.json"

#create a couple locker objects
locker = Locker(name='testlock', combo='32.51.0', address='1000 main street', host_number='5039895540', current_borrower_number='3335554444', checkout_time_length='14', start_date='9.5.2020', renewals_possible='1', renewals_used='1')
locker2 = Locker(name='testlock2', combo='32.51.0', address='1000 main street', host_number='5039895540', current_borrower_number='3335554444', checkout_time_length='14', start_date='9.5.2020', renewals_possible='1', renewals_used='1')
#serialize them
#reload them
#lkr = Locker

lockerobj_from_user_file = Lockers()
lockerobj_from_user_file.load_lockers_from_user_input_txt_file("template.txt")

lockerobj_from_user_file.print_lockers()
lockerobj_from_user_file.save_lockers_to_json_file('saving_lockers_to_json.txt')



#print "key: " + m.groups()[0] + "		value: " + m.groups()[1]
#m = re.search('^(\w+)\:(.+)\s+\#', line)
#raise Exception("Did not find a locker in " + locker_template_filename)


#locker_read_in = Locker(**locker_in_data)

#print "name: " + locker_read_in.name



#Next time add support for multiple lockers in the template







