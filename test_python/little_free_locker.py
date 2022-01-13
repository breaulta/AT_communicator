#!/usr/bin/python
import time
import serial
import re
import json
import os
from datetime import datetime, timedelta
import logging
mod_logger = logging.getLogger('LFL_app.little_free')

json_database = "locker_database.json"

#For holding multiple Locker objects.
#kwargs will hold locker name to locker object.
class Lockers:
	def __init__(self):
		self.lockers = []
		self.logger = logging.getLogger('LFL_app.little_free.Lockers')
		self.logger.info('creating locker bank')

	def _add_locker(self, locker):
		if self.does_locker_name_exist(locker.name):
			# Only used on startup
			raise Exception("Can't double add locker " + locker.name)
		self.lockers.append(locker)

	def _remove_locker(self, locker):
		if not self.does_locker_name_exist(locker.name):
			# Only used on startup
			raise Exception("We can't remove locker " + locker.name + " because it's not in our Lockers object")
		self.lockers.remove(locker)

	def print_lockers(self):
		for locker in self.lockers:
			print locker.name

	def get_locker_list(self):
		locker_list = []
		for locker in self.lockers:
			locker_list.append(locker.name)
		return locker_list

	def get_locker_obj_given_locker_name(self, locker_name):
		for locker in self.lockers:
			if locker_name == locker.name:
				return locker
		print "The locker with name " + locker_name + " was not found."

	def get_locker_obj_given_locker_number(self, locker_number):
		for locker in self.lockers:
			if locker.tenant_number != 'None':
				#print locker.tenant_number + " obj"
				if locker_number == locker.tenant_number:
					return locker
		print "The locker with number " + locker_number  + " was not found."

	def does_locker_name_exist(self, name):
		for locker in self.lockers:
			if name == locker.name:
				return 1
		return 0

	def save_lockers_to_json_file(self):
		locker_to_json = {}
		locker_to_json['lockers'] = []
		for locker in self.lockers:
			if hasattr(locker, 'logger'):
				del locker.logger
			locker_to_json['lockers'].append( vars(locker) ) #vars converts Locker object to dict
		outfile = open(json_database, 'w')
		json.dump(locker_to_json, outfile)
		outfile.close()

	#Create a Lockers object from our json database file.
	def json_file_to_lockers_obj(self):
		#Check if json database has been created before attempting to open.
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
			self._add_locker(new_locker_obj)

	#Update lockers retrieved from .json database with new attributes from template file.
	def populate_locker_attributes_from_template(self, locker_data_from_template_file):
		locker_name = locker_data_from_template_file['name']
		#Test if the locker already exists in our Lockers object
		if self.does_locker_name_exist(locker_name):
			locker_obj = self.get_locker_obj_given_locker_name(locker_name)
			#Remove the old version of the Locker object.
			self._remove_locker(locker_obj)
			for attribute in locker_data_from_template_file:
				setattr(locker_obj, attribute, locker_data_from_template_file[attribute])
			#Add our new version of the Locker object back onto the Lockers object.
			self._add_locker(locker_obj)
		#If it doesn't exist, create it anew.
		else:
			self._add_locker( Locker(**locker_data_from_template_file) )


	def load_lockers_from_user_input_txt_file(self, locker_template_filename):
		self.logger.info('pulling data from template...')
		#First run json_file_to_lockers_obj here, check for same locker names, and account for duplicates, to ensure that we're not creating duplicate lockers
		self.json_file_to_lockers_obj()
		#Hash to hold data gleaned from file for each locker.
		locker_in_data = {}
		locker_names_in_template_file = []
		template_file = open(locker_template_filename, 'r')
		for line in template_file:
			#Search for parameters of locker from template file.
			m = re.search('^(\w+)\:\"(.+)\"$', line)
			if m:
				#Working on the 'name' parameter.
				if m.groups()[0] == 'name':
					locker_name = m.groups()[1]
					#Check to make sure that two lockers with the same name don't appear in template file.
					if locker_name in locker_names_in_template_file:
						# Only used on startup
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
				self._remove_locker(locker)
		#Adding the last locker in the template file to our lockers object.
		if locker_in_data:
			self.populate_locker_attributes_from_template(locker_in_data)
		template_file.close()
		#Write any changes to Lockers object to json database.
		self.save_lockers_to_json_file()
		self.logger.info('completed pulling data from template file')

	# Not currently used
	def user_has_locker_checkedout (self, number):
		for locker in self.lockers:
			if locker.tenant_number != 'None':
				if locker.tenant_number == number:
					return 1
		return 0

	def is_locker_cluster_full (self):
		for locker in self.lockers:
			if locker.due_date == 'None':
				return 0
		return 1

	def earliest_possible_release (self):
		# Pick a date far in the future
		earliest = datetime(year=2100 , month=1, day=1)
		for locker in self.lockers:
			if locker.due_date == 'None':
				return 'Now.'
			else:
				trynext = locker.deserialize_date()
				diff = earliest - trynext
				seconds = diff.total_seconds()
				print 'secs: ' + str(seconds)
				if seconds >= 0: # 
					earliest = trynext
		return str(earliest)

	# This limits the number of lockers a tenant can checkout at one time to 1.
	# True/false returns are for tenant notification messages.
	def checkout_locker(self, number, lockername):
		for locker in self.lockers:
			#print 'tenant_number: ' + locker.tenant_number
			if locker.tenant_number == number:
				return 'duplicate number'
		locker = self.get_locker_obj_given_locker_name(lockername)
		if locker._checkout_locker_try(number):
			# Locker checkedout
			return 1
		else:
			# Exception would have triggered.
			return 'checked out'

	def list_available_lockers(self):
		available = ''
		for locker in self.lockers:
			if locker.tenant_number != 'None':
				continue
			else:
				available += locker.name + ' '
		if available == '':
			return 'No lockers available at this time. Earliest possible release: ' + self.earliest_possible_release()
		else:
			return available

	def freeup_locker(self, lockername):
		locker = self.get_locker_obj_given_locker_name(lockername)
		if not locker.is_locker_checked_out():
			raise Exception("Locker " + locker.name + " is already free!")
		else:
			locker.due_date = 'None'
			locker.tenant_number = 'None'
			locker.start_date = 'None'
			locker.renewals_used = '0'

#kwargs will hold locker attributes and values.
class Locker:
	def __init__(self, name, combo, address, host_number, checkout_time_length, total_renewals_possible,
				 start_date=None, due_date=None, tenant_number=None, renewals_used='0', onedayflag=None,
				 twodayflag=None):
		self.name = name
		self.combo = combo
		self.address = address
		self.host_number = host_number
		self.checkout_time_length = checkout_time_length
		self.total_renewals_possible = total_renewals_possible
		self.start_date = start_date
		self.due_date = due_date
		self.tenant_number = tenant_number
		self.renewals_used = renewals_used
		self.onedayflag = onedayflag
		self.twodayflag = twodayflag
		self.logger = logging.getLogger('test_logger_app.little_free.Locker')
		self.logger.info('creating locker')
	
	#Stringify a datetime object for storage in a json file.
	def serialize_date(self, datetime_object):
		serialized_date = str(datetime_object.month) + "/" + str(datetime_object.day) + "/" + str(datetime_object.year)
		return serialized_date

	#Return a datetime object from our json file.
	def deserialize_date(self):
		match_date = re.search('^(\d+)/(\d+)/(\d+)$', str(self.due_date))
		if match_date:
			month = int(match_date.groups()[0])
			day = int(match_date.groups()[1])
			year = int(match_date.groups()[2])
			return datetime(year=year, month=month, day=day)
		else:
			raise Exception("Improperly stored date: ~" + self.due_date + "~")

	def _checkout_locker_try(self, tenant_number):
		if self.is_locker_checked_out():
			return 0
		else:
			now = datetime.now()
			delta = timedelta(days=int(self.checkout_time_length))
			due_date = now + delta
			# Serialize datetime object.
			self.due_date = self.serialize_date(due_date)
			self.start_date = self.serialize_date(now)
			# record tenant number
			self.tenant_number = tenant_number
			self.renewals_used = '0'
			# set renewal flags
			self.onedayflag = 1
			self.twodayflag = 1
			return 1

	def is_locker_checked_out(self):
		if self.due_date == 'None':
			#Is checked out
			return 0
		else:
			return 1
	
	def renew_locker(self):
		# Ensure that locker is checked out.
		if not self.is_locker_checked_out():
			raise Exception("Can't renew locker " + self.name + ", it's not checked out!")
		# Ensure that we have renewals remaining
		if int(self.renewals_used) >= int(self.total_renewals_possible):
			raise Exception("Can't renew locker " + self.name + ", all renewals have already been used!")
		# Calculate new due date
		now = datetime.now()
		delta = timedelta(days=int(self.checkout_time_length))
		due_date = now + delta  # lsldhfslh
		# Serialize datetime object.
		self.due_date = self.serialize_date(due_date)
		# Increment renewals used up.
		self.renewals_used = str(int(self.renewals_used) + 1)

	def get_renewals_left(self):
		#print 'possible renewals: ' + self.total_renewals_possible + ' renewals used: ' + self.renewals_used
		return int(self.total_renewals_possible) - int(self.renewals_used)















