#!/usr/bin/python
#Don't create a pesky .pyc file.
import sys
sys.dont_write_bytecode = True
from little_free_locker import Locker


locker = Locker(name='testlock', combo='32.51.0', address='1000 main street', host_number='5039895540', current_borrower_number='3335554444', checkout_time_length='14', start_date='9.5.2020', renewals_possible='1', renewals_used='1')

print 'testing: checkout time length should be 14, it is actually: ' + locker.checkout_time_length


