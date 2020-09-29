#!/usr/bin/python
#Don't create a pesky .pyc file.
import re
import sys
sys.dont_write_bytecode = True
from little_free_locker import Locker
from little_free_locker import Lockers


lockerobj_from_user_file = Lockers()
#lockerobj_from_user_file.json_file_to_lockers_obj()
lockerobj_from_user_file.load_lockers_from_user_input_txt_file("template.txt")
#lockerobj_from_user_file.print_lockers()




#lockerobj_from_user_file.json_file_to_lockers_obj()
#print "\n\n"

#lockerobj_from_user_file.load_lockers_from_user_input_txt_file("template.txt")
#lockerobj_from_user_file.print_lockers()
#sample_locker = lockerobj_from_user_file.get_locker_obj_given_locker_name("LeBron")
#lockerobj_from_user_file.remove_locker(sample_locker)
#lockerobj_from_user_file.print_lockers()





#lockerobj_from_user_file.save_lockers_to_json_file()



#print "key: " + m.groups()[0] + "		value: " + m.groups()[1]
#m = re.search('^(\w+)\:(.+)\s+\#', line)
#raise Exception("Did not find a locker in " + locker_template_filename)


#locker_read_in = Locker(**locker_in_data)

#print "name: " + locker_read_in.name



#Next time add support for multiple lockers in the template







