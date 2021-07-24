#!/usr/bin/python
#Test receiving texts with pgsmm functionality.

#Don't write a pesky .pyc file.
import sys
sys.dont_write_bytecode = True

from module import Transmitter

print('Connect to modem.')
tx = Transmitter()

print('Create sms array of stored received texts.')
#new_sms_array = tx.get_all_texts()
sms_list = tx.get_all_texts()

print('Print all texts in array.')
for sms in sms_list:
	print('Number: ', sms.number, ' Message:')
	print(sms.text)
