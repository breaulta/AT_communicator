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

def json_file_to_locker_obj(self, filename):
		json_file = open(filename, 'r')
		read_data = json.load(json_file)
		json_file.close()
		#get list of lockers:
		locker_list = read_data['locker']
		#loop through first locker of list and append to object:
		repopulated_attributes = {}
		for locker_obj_attribute in locker_list[0]:
			key_to_value = locker_list[0][locker_obj_attribute]
			repopulated_attributes[locker_obj_attribute] = str(key_to_value)
		#Add attributes to new locker object.
		new_locker_obj = Locker(**repopulated_attributes)
		self = new_locker_obj
		return self



	


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

	def save_locker_obj_to_json_file(self, filename):
		data = {}
		data['locker'] = []
		#might need to check if these exist or it might error
		data['locker'].append({
			'name': self.name,
			'combo': self.combo,
			'address': self.address,
			'host_number': self.host_number,
			'current_borrower_number': self.current_borrower_number,
			'checkout_time_length': self.checkout_time_length,
			'start_date': self.start_date,
			'total_renewals_possible': self.total_renewals_possible,
			'renewals_used': self.renewals_used
		})
		outfile = open(filename, 'w')
		json.dump(data, outfile)
		outfile.close()
	
	def json_file_to_locker_obj(self, filename):
		json_file = open(filename, 'r')
		read_data = json.load(json_file)
		json_file.close()
		#get list of lockers:
		locker_list = read_data['locker']
		#loop through first locker of list and append to object:
		repopulated_attributes = {}
		for locker_obj_attribute in locker_list[0]:
			key_to_value = locker_list[0][locker_obj_attribute]
			repopulated_attributes[locker_obj_attribute] = str(key_to_value)
		#Add attributes to new locker object.
		new_locker_obj = Locker(**repopulated_attributes)
		self = new_locker_obj
		return self



#lockers with different passwords
#locker basic object
#each locker has combo, name, location, host contact number, current borrower phone number, 
#locker checkout time, options to renew, number of renewals possible.
#Maybe locker block object that holds multiple lockers on the same sim/modem.
#update owner with texts
#combos for lockers saved in text file maybe

