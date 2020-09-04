#!/usr/bin/python
#Don't create a pesky .pyc file.
import os
import sys
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
