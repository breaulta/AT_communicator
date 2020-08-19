#!/usr/bin/python
#Don't create a pesky .pyc file.
import sys
sys.dont_write_bytecode = True
from module import Transmitter
from module import SMS

tx = Transmitter(port = '/dev/ttyUSB2')
#tx.send_text('5033803136', '2nd from python')

#delete_result = tx.delete_text('1')
#print "delete result: ", delete_result, "\n"

"""
response = tx.get_all_texts()
for sms in response:
	print "phone: ", sms.index, "\n"
#print "sms_obj: ", sms_obj.index, "\n"

"""


text_array = tx.get_all_texts()
tx.save_sms_obj_to_json_file(text_array, "special.txt")
sms_array = tx.json_file_to_sms_array("special.txt")

for sms in sms_array:
	print "message: ", sms.message, "\n"

