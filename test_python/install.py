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
rc_local_file.close()
rc_local_fd = open("/etc/rc.local", "w")
for line in rc_local_list:
	if line == 'exit(0)':
		#print "cd " + run_directory
		rc_local_fd.write("cd " + run_directory)
		#print "sudo python " + run_directory + " " + main_script
		rc_local_fd.write("sudo python " + run_directory + " " + main_script)
	#print "~~~" + line + "~~~"
	rc_local_fd.write(line)


#insert cd into our main directory
#insert 'python /path/mainfile.py &'
#

