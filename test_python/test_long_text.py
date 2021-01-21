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
tx.send_text('5039895540', 'This is a very long text that I would like to make into a long text. This is a very long text that I would like to make into a long text. This is a very long text that I would like to make into a long text. This is a very long text that I would like to make into a long text. This is a very long text that I would like to make into a long text. This is a very long text that I would like to make into a long text. This is a very long text that I would like to make into a long text. This is a very long text that I would like to make into a long text. This is a very long text that I would like to make into a long text. This is a very long text that I would like to make into a long text. This is a very long text that I would like to make into a long text.')
