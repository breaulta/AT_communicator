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
ch.setLevel(logging.ERROR)
# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(fh)
logger.addHandler(ch)

from little_free_locker import Locker
from little_free_locker import Lockers

logger.info('create lockers object')
locker_bank = Lockers()
logger.info('load from template')
locker_bank.load_lockers_from_user_input_txt_file("template.txt")

nala = locker_bank.get_locker_object_given_locker_name('Nala')
nala.freeup_locker
#logger.info('end')




