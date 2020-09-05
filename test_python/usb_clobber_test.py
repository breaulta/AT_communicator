#!/usr/bin/python
#Don't create a pesky .pyc file.
import os
import sys
import re
import time
sys.dont_write_bytecode = True

sim_path = '/dev/cdc-wdm0'
print 'turn online'
os.system("qmicli -d " + sim_path + " --dms-set-operating-mode='online'")
time.sleep(20)
print 'set to reset'
os.system("qmicli -d " + sim_path + " --dms-set-operating-mode='reset'")
time.sleep(20)
print 'turn back online'
os.system("qmicli -d " + sim_path + " --dms-set-operating-mode='online'")

get_qmicli_mode(sim_path)

def get_qmicli_mode(sim_path):
	count = 0
	while count < 100000:
		get_output = os.popen('qmicli -d ' + sim_path + ' --dms-get-operating-mode')
		output_read = get_output.read()
		mode_match = re.search("Mode: '([a-z-]+)'", output_read)
		if mode_match.group(1) is not None:
			return mode_match.group(1)
		else:
			return 0

