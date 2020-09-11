#!/usr/bin/python
#Don't create a pesky .pyc file.
import sys
sys.dont_write_bytecode = True
import os

run_directory = "/home/pi/communicator/test_python"
main_script = "startup_test.py"
#run through the rc.local file until it hits exit(0)
rc_local_file = open("/etc/rc.local", "r")
rc_local_content = rc_local_file.read()
rc_local_list = rc_local_content.split("\n")
for line in rc_local_list:
	if line == 'exit(0)':
		print "cd " + run_directory
		print "sudo python " + run_directory + " " + main_script
	print "~~~" + line + "~~~"

#insert cd into our main directory
#insert 'python /path/mainfile.py &'
#

