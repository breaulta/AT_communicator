#!/usr/bin/python
#Don't create a pesky .pyc file.
import sys
sys.dont_write_bytecode = True
from module import Transmitter
from module import SMS

tx = Transmitter(port = '/dev/ttyUSB2')
#tx.send_text('5033803136', '2nd from python')

delete_result = tx.delete_text('1')
print "delete result: ", delete_result, "\n"

"""
response = tx.get_all_texts()
for sms in response:
	print "phone: ", sms.index, "\n"
#print "sms_obj: ", sms_obj.index, "\n"

"""
