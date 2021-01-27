#!/usr/bin/python
# -*- coding: utf-8 -*-
#Don't write a pesky .pyc file.
import sys
sys.dont_write_bytecode = True

from module import Transmitter
from module import SMS
from little_free_locker import Locker
from little_free_locker import Lockers


tx = Transmitter()
tx.send_text('5039895540', "Hey Len~! I hope you're doing well.  This is Aaron and I'm doing fine thank you.  As you can see(hopefully!) I have been able to get the PDU formatted long text (Concatenated Short Message) working.  Before I moved on to the next step in the project I thought it would be a good idea to go over some of the decisions I've made and update you on how the project is going.  If 9AM is still a good time for you, I am available to meet tomorrow, Friday, or early next week as you like. Some chars in the extended gsm7 alphabet: |^[]{}  Please RSVP to Aaron's regular number.  Thanks!")
