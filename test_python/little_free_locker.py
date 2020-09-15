#!/usr/bin/python
import time
import serial
import re
import json
import os

class Little_free_locker:
	def __init__(self, **kwargs):
        if 'name' in kwargs:
            self.name = kwargs['name']
        else:
			raise Exception ("The locker needs a name.")
        if 'combo' in kwargs:
            self.combo = kwargs['combo']
        else:
			raise Exception ("The locker needs a combo.")
        if 'address' in kwargs:
            self.address = kwargs['address']
        else:
			raise Exception ("The locker needs an address.")
        if 'host_number' in kwargs:
            self.host_number = kwargs['host_number']
        else:
			raise Exception ("The locker needs a contact number for the host.")
        if 'current_borrower_number' in kwargs:
            self.current_borrower_number = kwargs['current_borrower_number']
        if 'checkout_time_length' in kwargs:
            self.checkout_time_length = kwargs['checkout_time_length']
        else:
			raise Exception ("The locker needs to know how long to be active per user session.")
        if 'start_date' in kwargs:
            self.start_date = kwargs['start_date']
        if 'end_date' in kwargs:
            self.end_date = kwargs['end_date']
        if 'total_renewals_possible' in kwargs:
            self.total_renewals_possible = kwargs['total_renewals_possible']
		else:
			self.total_renewals_possible = 0
        if 'renewals_used' in kwargs:
            self.renewals_used = kwargs['renewals_used']
		else:
			self.renewals_used = 0



#lockers with different passwords
#locker basic object
#each locker has combo, name, location, host contact number, current borrower phone number, 
#locker checkout time, options to renew, number of renewals possible.
#Maybe locker block object that holds multiple lockers on the same sim/modem.
#update owner with texts
#combos for lockers saved in text file maybe

