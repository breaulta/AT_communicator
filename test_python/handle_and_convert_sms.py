#!/usr/bin/python
import time
from datetime import datetime, timedelta
import serial
import re
import json
import os
import sys
#Don't write a pesky .pyc file.
sys.dont_write_bytecode = True
#for testing
import threading

from module import SMS



path = './incoming_sms'

def delay_make_a_file():
	time.sleep(5)
	# test input sms object
	sms = SMS('1', 'ok', '5039895540', '1/4/2022', 'manual test sms msg')

	# write object datas to file
	# Create dir if it doesn't already exist.
	try:
		os.makedirs(path)
	except OSError:
		if not os.path.isdir(path):
			raise Exception('dir not created for some reason')
	filename = path + '/' + sms.index + '_new_sms.txt'

	# If it opens, it exists => fail.
	try:
		f = open(filename)
	# Working properly.
	except IOError:
		f = open(filename, 'w')
		sms_list = str(vars(sms))
		f.write(sms_list)
		f.close
	else:
		raise Exception('Generated file for incoming SMS should not already exist!')
	
# main loop periodically scans a folder for a new file with unique name
def main():
	thread = threading.Thread(target=delay_make_a_file())
	thread.start()
	while 1:
		dirlist = os.listdir(path)
		if not dirlist:
			print 'found no new file'
		else:
			m = re.search('\d+_new_sms.txt', dirlist[0])
			if m:
				fil = path + '/' + dirlist[0]
				fd = open(fil, 'r')
				print fd.read()
				fd.close()
				os.remove(fil)
			else:
				print 'found a non-matching file'
		time.sleep(1)

# when one is found, scan in the datas and delete file

# act on the datas

if __name__ == '__main__':
    main()










