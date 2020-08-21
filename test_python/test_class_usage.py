#!/usr/bin/python

#Don't create a pesky .pyc file.
import sys
sys.dont_write_bytecode = True

#Import classes to deal with SIM card and SMS objects
from module import Transmitter
from module import SMS

sms_database_filename = "sms_database.json"

tx = Transmitter(port = '/dev/ttyUSB2')
#tx.send_text('5033803136', '4th from python')

#Get new sms messages from SIM card in array.
new_sms_array = tx.get_all_texts()

print "array number: ", len(new_sms_array), "\n"
exit(0)

#If we have new texts.
if len(new_sms_array) > 0:
	#Write new sms messages to database.
	#First check if sms database file exists.
	try:
		open(sms_database_filename)
	#If doesn't exist create it and write new sms messages to it.
	except IOError:
		tx.save_sms_obj_to_json_file(new_sms_array, sms_database_filename)
	#Read the texts from our text message database json file.
	else:
		db_sms_array = tx.json_file_to_sms_array(sms_database_filename)
		full_db_sms_array = db_sms_array + new_sms_array 
		tx.save_sms_obj_to_json_file(full_db_sms_array, sms_database_filename)
#We have no new texts.
else:
	print "we have no new texts\n"


"""




#delete_result = tx.delete_text('1')

response = tx.get_all_texts()
for sms in response:
	print "phone: ", sms.index, "\n"
#print "sms_obj: ", sms_obj.index, "\n"
print "I'm not running am I?\n"


text_array = tx.get_all_texts()
tx.save_sms_obj_to_json_file(text_array, "special.txt")
sms_array = tx.json_file_to_sms_array("special.txt")

#for sms in sms_array:
#	print "message: ", sms.message, "\n"

print "I'm not running am I?\n"
"""
