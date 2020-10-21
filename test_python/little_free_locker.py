#!/usr/bin/python
import time
import serial
import re
import json
import os
from datetime import datetime, timedelta

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
			if self.does_locker_name_exist(new_locker_obj.name):
				continue
			#Add to Lockers list of lockers
			self.add_locker(new_locker_obj)

	#Update lockers retrieved from .json database with new attributes from template file.
	def populate_locker_attributes_from_template(self, locker_data_from_template_file):
		locker_name = locker_data_from_template_file['name']
		#Test if the locker already exists in our Lockers object
		if self.does_locker_name_exist(locker_name):
			locker_obj = self.get_locker_obj_given_locker_name(locker_name)
			#Remove the old version of the Locker object.
			self.remove_locker(locker_obj)
			for attribute in locker_data_from_template_file:
				setattr(locker_obj, attribute, locker_data_from_template_file[attribute])
			#Add our new version of the Locker object back onto the Lockers object.
			self.add_locker(locker_obj)
		#If it doesn't exist, create it anew.
		else:
			self.add_locker( Locker(**locker_data_from_template_file) )


	def load_lockers_from_user_input_txt_file(self, locker_template_filename):
		#First run json_file_to_lockers_obj here, check for same locker names, and account for duplicates, to ensure that we're not creating duplicate lockers
		self.json_file_to_lockers_obj()
		#Hash to hold data gleaned from file for each locker.
		locker_in_data = {}
		locker_names_in_template_file = []
		infile = open(locker_template_filename, 'r')
		for line in infile:
			#Search for parameters of locker.
			m = re.search('^(\w+)\:\"(.+)\"$', line)
			if m:
				#Working on the 'name' parameter.
				if m.groups()[0] == 'name':
					locker_name = m.groups()[1]
					#Check to make sure that two lockers with the same name don't appear in template file.
					if locker_name in locker_names_in_template_file:
						raise Exception("Locker name " + locker_name + " appears more than once in the file!")
					else:
						locker_names_in_template_file.append(locker_name) 
					#We're on a new locker in our template file.
					#Write stored data from previous loop to lockers object. 
					if locker_in_data:
						self.populate_locker_attributes_from_template(locker_in_data)
					#Start populating new locker hash(dict).
					locker_in_data = {} #Reset for new locker.
					locker_in_data.update({"name":locker_name})
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
		#Remove any lockers not represented in the template file (master).
		for locker in self.lockers:
			if locker.name not in locker_names_in_template_file:
				self.remove_locker(locker)
		#Adding the last locker in the template file to our lockers object.
		if locker_in_data:
			self.populate_locker_attributes_from_template(locker_in_data)
		infile.close()
		#Write any changes to Lockers object to json database.
		self.save_lockers_to_json_file()

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
		
	
	#Stringify a datetime object for storage in a json file.
	def serialize_date(self, datetime_object):
		serialized_date = str(datetime_object.month) + "/" + str(datetime_object.day) + "/" + str(datetime_object.year)
		return serialized_date

	#Return a datetime object from our json file.
	def deserialize_date(self, serialized_date):
		match_date = re.search('^(\d+)/(\d+)/(\d+)$', serialized_date)
		if match_date:
			month = int(match_date.groups()[0])
			day = int(match_date.groups()[1])
			year = int(match_date.groups()[2])
			return datetime(year=year, month=month, day=day)
		else:
			raise Exception("Improperly stored date: ~" + serialized_date + "~")

	#Calculate due date based on difference between current time and checkout length.
	def checkout_locker(self):
		now = datetime.now()
		delta = timedelta(days=int(self.checkout_time_length))
		due_date = now + delta
		#Serialize datetime object.
		self.due_date = self.serialize_date(due_date)

	def is_locker_checked_out(self):
		if hasattr(self, "due_date"):
			#Is checked out
			return 1
		else:
			return 0
		

	#def checkout_locker(self):
		#check if checked out
		#set checkout date
		#calc duedate
		#save duedate
		

#Notes for next time:
#   Calculate due_date in locker method for is_locker_checked_out method
#   Create is_locker_checked_out method
#   Create checkout_locker method
#   


#lockers with different passwords
#locker basic object
#each locker has combo, name, location, host contact number, current borrower phone number, 
#locker checkout time, options to renew, number of renewals possible.
#Maybe locker block object that holds multiple lockers on the same sim/modem.
#update owner with texts
#combos for lockers saved in text file maybe

