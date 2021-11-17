#!/usr/bin/python
import time
#from datetime import datetime, timedelta
import json
import os
#Don't write a pesky .pyc file.
import sys
sys.dont_write_bytecode = True

from little_free_locker import Locker
from little_free_locker import Lockers

locker_bank = Lockers() #init
mylocker = Locker('aaron') #init

locker_bank.add_locker(mylocker)

locker_bank.get_locker_obj_given_locker_name('aaron')
