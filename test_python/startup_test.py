#!/usr/bin/python
#Don't create a pesky .pyc file.
import sys
sys.dont_write_bytecode = True
import os

path = '/home/pi/communicator/test_python/test_startup'
filepath = os.path.join(path, 'python_startup_test_success')
if not os.path.exists(path):
    os.makedirs(path)
f = open(filepath, "a")
