#!/usr/bin/python
#This file sets up the pi to auto-start into our handler.
#Don't create a pesky .pyc file.
import sys
sys.dont_write_bytecode = True
import os
import re

run_directory = "/home/pi/communicator/test_python"
main_script = "startup_test.py"
#run through the rc.local file until it hits exit(0)
rc_local_file = open("/etc/rc.local", "r")
rc_local_content = rc_local_file.read()
rc_local_list = rc_local_content.split("\n")
#Check to make sure we're not installing to rc.local twice
for line in rc_local_list:
	if re.search(main_script, line):
		#don't rewrite lines to rc.local
		exit(0)

rc_local_file.close()
rc_local_fd = open("/etc/rc.local", "w")
for line in rc_local_list:
	if line == 'exit 0':
		rc_local_fd.write("cd " + run_directory + "\n")
		rc_local_fd.write("sudo python " + run_directory + "/" + main_script + "\n")
	rc_local_fd.write(line + "\n")


#insert cd into our main directory
#insert 'python /path/mainfile.py &'
#add regex to make see if we've already writen the necessary lines to rc.local

