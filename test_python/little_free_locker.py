#!/usr/bin/python
import time
import serial
import re
import json
import os

#For holding multiple Locker objects.
#kwargs will hold locker name to locker object.
class Lockers:
	def __init__(self):
		self.lockers = []

	def add_locker(self, locker):
		self.lockers.append(locker)

	def print_lockers(self):
		for locker in self.lockers:
			print locker.name

	def save_lockers_to_json_file(self, filename):
		locker_to_json = {}
		locker_to_json['lockers'] = []
		for locker in self.lockers:
			locker_to_json['lockers'].append( vars(locker) ) #vars converts Locker object to dict
		outfile = open(filename, 'w')
		json.dump(locker_to_json, outfile)
		outfile.close()

	def json_file_to_lockers_obj(self, filename):
		json_file = open(filename, 'r')
		read_data = json.load(json_file)
		json_file.close()
		#get list of lockers:
		locker_list = read_data['lockers']
		#loop through first locker of list and append to object:
		for locker in locker_list:
			locker_dict = {}
			for locker_obj_attribute in locker:
				key_to_value = locker[locker_obj_attribute]
				locker_dict[locker_obj_attribute] = str(key_to_value)
			#Add attributes to new locker object.
			new_locker_obj = Locker(**locker_dict)
			#Add to Lockers list of lockers
			self.add_locker(new_locker_obj)

#kwargs will hold locker attributes and values.
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


#lockers with different passwords
#locker basic object
#each locker has combo, name, location, host contact number, current borrower phone number, 
#locker checkout time, options to renew, number of renewals possible.
#Maybe locker block object that holds multiple lockers on the same sim/modem.
#update owner with texts
#combos for lockers saved in text file maybe

