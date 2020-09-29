#!/usr/bin/python
import time
import serial
import re
import json
import os

json_database = "locker_database.json"

#For holding multiple Locker objects.
#kwargs will hold locker name to locker object.
class Lockers:
	def __init__(self):
		self.lockers = []

	def add_locker(self, locker):
		self.lockers.append(locker)

	def remove_locker(self, locker):
		self.lockers.remove(locker)

	def print_lockers(self):
		for locker in self.lockers:
			print locker.name

	def get_locker_obj_given_locker_name(self, locker_name):
		for locker in self.lockers:
			if locker_name == locker.name:
				return locker
		print "The locker with name " + locker_name + "was not found."

	def does_locker_name_exist(self, name):
		for locker in self.lockers:
			if name == locker.name:
				return 1
		return 0

	def save_lockers_to_json_file(self):
		locker_to_json = {}
		locker_to_json['lockers'] = []
		for locker in self.lockers:
			locker_to_json['lockers'].append( vars(locker) ) #vars converts Locker object to dict
		outfile = open(json_database, 'w')
		json.dump(locker_to_json, outfile)
		outfile.close()

	def json_file_to_lockers_obj(self):
		#It's ok if it hasn't been created yet, test for existence, and exit here.
		if not os.path.isfile(json_database):
			return	
		json_file = open(json_database, 'r')
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

#FOR NEXT TIME:
#After we load in the json file locker list, make sure that all of the lockers in the json file
#are still present in the template file.
#If a locker name has been removed from the template file, remove it from our Lockers object.

#Also, we want to be overwriting any Locker attributes that are specified in the template file
#(e.g. the user changes the combo)

	def load_lockers_from_user_input_txt_file(self, locker_template_filename):
		#First run json_file_to_lockers_obj here, check for same locker names, and account for duplicates, to ensure that we're not creating duplicate lockers
		self.json_file_to_lockers_obj()
		#Hash to hold data gleaned from file for each locker.
		locker_in_data = {}
		check_for_locker_name_duplicates = []
		infile = open(locker_template_filename, 'r')
		for line in infile:
			#Search for parameters of locker.
			m = re.search('^(\w+)\:\"(.+)\"$', line)
			#We found 'name' the beginning of locker parameters.
			if m:
				if m.groups()[0] == 'name':
					locker_name = m.groups()[1]
					#Check to make sure that two lockers with the same name don't appear in template file.
					if locker_name in check_for_locker_name_duplicates:
						raise Exception("Locker name " + locker_name + " appears more than once in the file!")
					else:
						check_for_locker_name_duplicates.append(locker_name) 
					#Test if this locker has already been added to database.
					if self.does_locker_name_exist(locker_name):
						continue
					#Test if we have a different locker stored.
					if locker_in_data:
						#If so, add it to the Lockers object.
						self.add_locker( Locker(**locker_in_data) )
					locker_in_data = {} #Reset for new locker.
					locker_key = m.groups()[0]
					locker_value = m.groups()[1]
					locker_in_data.update({locker_key:locker_value})
				#We found a different locker aspect from 'name'.
				else:
					#If no name here, it's not a valid locker object, so move on.
					if locker_in_data.has_key("name"):
						locker_key = m.groups()[0]
						locker_value = m.groups()[1]
						locker_in_data.update({locker_key:locker_value})
					else:
						continue
			#We did not match, move onto the next locker or to the end of file.
			else:
				continue
		if locker_in_data:
			self.add_locker( Locker(**locker_in_data) )
		infile.close()


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
			self.total_renewals_possible = "0"
		if 'renewals_used' in kwargs:
			self.renewals_used = kwargs['renewals_used']
		else:
			self.renewals_used = "0"


#lockers with different passwords
#locker basic object
#each locker has combo, name, location, host contact number, current borrower phone number, 
#locker checkout time, options to renew, number of renewals possible.
#Maybe locker block object that holds multiple lockers on the same sim/modem.
#update owner with texts
#combos for lockers saved in text file maybe

