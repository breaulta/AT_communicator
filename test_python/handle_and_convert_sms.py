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
	#time.sleep(5)
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
		#sms_list = str(vars(sms))
		sms_dict = vars(sms)
		json.dump(sms_dict, f)
		#f.write(sms_list)
		f.close
	else:
		raise Exception('Generated file for incoming SMS should not already exist!')
	
# main loop periodically scans a folder for a new file with unique name
def main():
	delay_make_a_file()
	while 1:
		if os.path.isdir(path):
			dirlist = os.listdir(path)
			if not dirlist:
				print 'found no new file'
			else:
				# allows for other files in the dir to not break it.
				for filename in dirlist:
					match = re.search('\d+_new_sms.txt', filename)
					if match:
						#fil = path + '/' + dirlist[0]
						fil = path + '/' + filename
						fd = open(fil, 'r')
						#print fd.read()
						# create SMS object and store data there
						#newSms = SMS()
						json_read_dict = json.load(fd)
						fd.close()
						os.remove(fil)
						sms = SMS(**json_read_dict)
						print sms.index
					else:
						print 'found a non-matching file'
		else:
			print 'dir not created'
		time.sleep(1)

# when one is found, scan in the datas and delete file

# act on the datas

if __name__ == '__main__':
    main()










