#!/usr/bin/python
import time
import serial
import re
import json
import os

class Locker:
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
		if 'total_renewals_possible' in kwargs:
			self.total_renewals_possible = kwargs['total_renewals_possible']
		else:
			self.total_renewals_possible = 0
		if 'renewals_used' in kwargs:
			self.renewals_used = kwargs['renewals_used']
		else:
			self.renewals_used = 0

	def save_locker_obj_to_json_file(self, filename):
		data = {}
		data['locker'] = []
		#might need to check if these exist or it might error
		data['locker'].append({
			'name': self.locker.name,
			'combo': self.locker.combo,
			'address': self.locker.address,
			'host_number': self.locker.host_number,
			'current_borrower_number': self.locker.current_borrower_number,
			'checkout_time_length': self.locker.checkout_time_length,
			'start_date': self.locker.start_date,
			'total_renewals_possible': self.locker.total_renewals_possible,
			'renewals_used': self.locker.renewals_used
		})
		outfile = open(filename, 'w')
		json.dump(data, outfile)
		outfile.close()
	
	def json_file_to_locker_array(self, filename):
		json_file = open(filename, 'r')
		read_data = json.load(json_file)
		json_file.close()
		for locker_json in read_data['locker']:
			locker_obj = Locker(
				locker_json['name'],
				locker_json['combo'],
				locker_json['address'],
				locker_json['host_number'],
				locker_json['current_borrower_number'],
				locker_json['checkout_time_length'],
				locker_json['start_date'],
				locker_json['total_renewals_possible'],
				locker_json['renewals_used']
			)
		return locker_obj





#lockers with different passwords
#locker basic object
#each locker has combo, name, location, host contact number, current borrower phone number, 
#locker checkout time, options to renew, number of renewals possible.
#Maybe locker block object that holds multiple lockers on the same sim/modem.
#update owner with texts
#combos for lockers saved in text file maybe

