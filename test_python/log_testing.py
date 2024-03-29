#!/usr/bin/python
import time
from datetime import datetime, timedelta
import serial
import re
import json
import os
#Don't write a pesky .pyc file.
import sys
sys.dont_write_bytecode = True

import logging
logger = logging.getLogger('test_logger_app')
logger.setLevel(logging.DEBUG)	# Set default level?
# create file handler which logs even debug messages
fh = logging.FileHandler('locker.log')
fh.setLevel(logging.DEBUG)
# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(fh)
logger.addHandler(ch)

from streamtologger import StreamToLogger
stdout_logger = logging.getLogger('test_logger_app')
sl = StreamToLogger(stdout_logger, logging.INFO)
sys.stdout = sl

stderr_logger = logging.getLogger('test_logger_app')
sl = StreamToLogger(stderr_logger, logging.ERROR)
sys.stderr = sl

#print "Test to standard out"
#raise Exception('Test to standard error')

from little_free_locker import Locker
from little_free_locker import Lockers

print "to stdout please~!"

logger.info('create lockers object')
locker_bank = Lockers()
logger.info('load from template')
locker_bank.load_lockers_from_user_input_txt_file("template.txt")

locker_bank.checkout_locker('5039895540', 'ala')

locker_bank.freeup_locker('Nala')
#nala = locker_bank.get_locker_object_given_locker_name('Nala')
#nala.freeup_locker
#logger.info('end')




