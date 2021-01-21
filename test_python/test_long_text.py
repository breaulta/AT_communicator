#!/usr/bin/python
#Don't write a pesky .pyc file.
import sys
sys.dont_write_bytecode = True

from module import Transmitter
from module import SMS
from little_free_locker import Locker
from little_free_locker import Lockers


tx = Transmitter()
tx.send_text('5039895540', 'Major changes/decisions I’ve made that I would like to go over with Len
Hard coding UDH/Fill bits in the PDU because we are only going to use it for sending Concatenated SMS
Piecing together elements of a couple different scripts in order to implement PDU CSM.
I found a whole gsm modem implementation that we could have potentially used at the beginning, but ended up taking pieces of the lower level code.
8-bit is not a possibility as it doesn’t have an alphabet attached to it.
Aaron dont ever forget how much of a beast your are XD')
