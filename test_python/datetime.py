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

from module import Transmitter
from module import SMS
from little_free_locker import Locker
from little_free_locker import Lockers

now = datetime.now()

delta = timedelta(days=7)

dude_date = now + delta

print "now: " + now + " delta: " + delta + " dude_date: " + due_date