#!/usr/bin/python
import time
import serial
import re
import json
import os
 
class Transmitter:
	#Initalize Transmitter object attributes.
	def __init__(self, **kwargs):
		#Ensure that we're running as root.
		if not os.geteuid()==0:
			raise Exception("Must run as root!")
		#If a specific port is specified, connect to that port.
		defined_port = ''
		if 'port' in kwargs:
			defined_port = kwargs['port']
		else:
			defined_port = '/dev/ttyUSB2'
		self.usb_path = defined_port
		self.__configure_ser_connection_to_usb(self.usb_path)
		#If a specific QMICLI device path is specified, use that.
		defined_qmi_path = ''
		if 'qmi_path' in kwargs:
			defined_qmi_path = kwargs['qmi_path']
		else:
			defined_qmi_path = '/dev/cdc-wdm0'
		self.ensure_sim_card_connected_to_network(defined_qmi_path)

	#Configure serial connection settings.
	def __configure_ser_connection_to_usb(self, usb_port):
		self.ser = serial.Serial(
			port=usb_port,
			baudrate=9600,
			parity=serial.PARITY_NONE,
			stopbits=serial.STOPBITS_TWO,
			bytesize=serial.EIGHTBITS
		)
		time.sleep(5)
		#Ensure that AT command 'AT' returns echoed 'AT' (multiple tries if necessary).
		for connection_attempt in range(15):
			check_AT = self.send_AT('AT')
			#Ensure that AT message is returned.
			if check_AT:
				if check_AT.startswith('AT'):
					return
				else:
					time.sleep(5)
			else:
				time.sleep(15)
		raise Exception("Hey, we did not expect this AT test to fail!")
		


	#Check that the SIM card via the Qmicli interface is connected to the mobile network.
	#Default for raspberry pi + waveshare SIM7600 Hat is /dev/cdc-wdm0
	#Must run as root
	def ensure_sim_card_connected_to_network(self, sim_path):
		#Check if our SIM card is connected to the network or not.
		sim_mode = self.__get_qmicli_mode(sim_path)
		#If not online, try to turn it on.
		if sim_mode != "online":
			#If sim/modem is reset when the serial connection is open, it will clobber /dev/ttyUSB2.
			#So we close the serial connection while we perform the reset.
			if self.ser.isOpen() == True:
				self.ser.close()
			print "Sim card was off, turning online."
			self.__set_qmicli_mode('online', sim_path)
			timeout_count = 0
			#Verify that it comes online.
			while(1):
				time.sleep(10)
				sim_mode = self.__get_qmicli_mode(sim_path)
				if sim_mode == 'online':
					#We're online! Escape bonds of while loop and return.
					print "Successfuly set sim card online."
					break
				#Otherwise, let's try to turn it online.
				else:
					print "Sim card is being reset to turn it online."
					time.sleep(10)
					self.__set_qmicli_mode('reset', sim_path)
					time.sleep(30)
					#For potential debugging. We expect SIM mode = 'low-power' here after reset.
					get_response = self.__get_qmicli_mode(sim_path)
					if 'low-power' != get_response:
						print "Warning, SIM Mode is: " + get_response
					else:
						print "We're in low power mode, please wait as we turn SIM online."
					time.sleep(1)
					self.__set_qmicli_mode('online', sim_path)
					time.sleep(20)
					timeout_count += 1
					#Time out after a few minutes of trying
					if timeout_count > 2:
						raise Exception("The SIM card could not be set to online mode!")
			#Turn serial connection back on after resetting sim/modem.
			self.__configure_ser_connection_to_usb(self.usb_path)
			return 1
		#Looks like we're online! Return true.
		else:
			return 1

	#Check to make sure the sim_path exists, which implies that the modem can accept qmicli commands
	def __check_sim_path(self, sim_path):
		#qmicli clobbers path during 'reset' so the while loop ensures no false negatives.
		timeout_count = 0
		while timeout_count < 15:
			#Ensure that path to SIM card exists.
			if os.path.exists(sim_path):
				return 1
			else:
				time.sleep(1)
				timeout_count += 1
		raise Exception("The SIM card path " + sim_path + " does not exist!")

	#Sets our SIM card to the specified mode (e.g. 'reset', 'online', etc).
	def __set_qmicli_mode(self, mode, sim_path):
		self.__check_sim_path(sim_path)
		os.system("qmicli -d " + sim_path + " --dms-set-operating-mode='" + mode + "'")
	
	#Returns SIM card mode (e.g. 'offline', 'online', 'low-power', 'reset', etc.
	def __get_qmicli_mode(self, sim_path):
		self.__check_sim_path(sim_path)
		get_output = os.popen('qmicli -d ' + sim_path + ' --dms-get-operating-mode')
		output_read = get_output.read()
		mode_match = re.search("Mode: '([a-z-]+)'", output_read)
		if mode_match.group(1) is not None:
			return mode_match.group(1)
		else:
			print "Error: we could not read mode for:\n" + output_read
			return 0

    #Send AT command to modem.
	def send_AT(self, AT):
		#Open up our serial connection to the SIM
		self.ser.isOpen()   
		#First send a simple 'AT' command, and confirm it returns 'OK'.
		#This will indicate to us that our SIM is working and ready for more AT commands.
		for filter_AT_response in range(15):
			print "inside infinite while"
			ok_response = ''
			self.ser.write("AT\r\n")
			while self.ser.inWaiting() > 0:
				ok_response += self.ser.read(1)
			if ok_response.startswith('AT'):
				break
			time.sleep(5)
			if filter_AT_response > 14:
				raise Exception('Could not verify AT functionality by an AT echo')
		self.ser.write(AT + "\r\n")
		time.sleep(1)
		ser_response = ''
		while self.ser.inWaiting() > 0:
			ser_response += self.ser.read(1)
		return ser_response

	#Check if SIM card configured for SMS text mode.
	def check_sms_mode(self):
		sms_mode = self.send_AT('AT+CMGF?')
		regex_mode_result = re.search("\+CMGF:\s+([01])", sms_mode)
		if regex_mode_result:
			#If CMGF = 1, our sim is in text mode
			if regex_mode_result.group(1) == '1':
				return "text_mode_on"
			#If CMGF = 0, our sim is in pdu mode
			elif regex_mode_result.group(1) == '0':
				return "text_mode_off"
		#We ran into this bug once before, hopefully we can narrow it down with this exception:
		raise Exception("Error: our CMGF query didn't return 1 or 0, here's what we got back: ~" + sms_mode + "~")

    #Set SMS for text mode. sms_mode of 1 = texting (this is what we want), 0 = Programmable data unit PDU.
	def set_sms_mode(self, sms_mode):
		sms_mode = str(sms_mode) #convert num to string
		sms_mode_response = self.send_AT('AT+CMGF=' + sms_mode)
		ok = re.findall("OK", sms_mode_response)
		if (not ok):
			raise Exception("SMS mode ", sms_mode, " was not successfully set\n")

	#Sends a text to the specified number, with the specified message.
	def send_text(self, number, message):
		#Make sure texting is turned on in the SIM card.
		current_sms_mode = self.check_sms_mode()
		if current_sms_mode == "text_mode_off":
			set_sms_mode("1")
		elif current_sms_mode == "text_mode_error":
			raise Exception("SMS mode query error. There may be a problem with modem communication.")
		#Send the modem the CMGS command in the format to send a text out, where chr(26) is the required ctrl+Z that denotes EOF
		response1 = self.send_AT('AT+CMGS="' + number + '"\r\n') 
		response2 = self.send_AT( message + chr(26))

	def send_text_to_host(self, host_number, tenant_number, message):
		host_message = "Text sent to ~" + tenant_number +"~ :\n" + message 
		self.send_text(host_number, host_message)

	#Returns array of SMS objects, returning all texts on SIM card.
	def get_all_texts(self):
		sms_array = []
		text_list = self.send_AT('AT+CMGL="ALL"')
		text_array = text_list.split('+CMGL:')
		for text_array_index, text in enumerate(text_array):
			text_regex = '^\s*([0-9]+),\"([A-Z\s]+)\",\"\+?1?([0-9]{10})\",\"[^\"]*\",\"([^\"]+)\"\s+(.*)$'	
			re_result = re.search(text_regex, text, re.DOTALL)
			if re_result:
				index = re_result.group(1)
				status = re_result.group(2)
				phone = re_result.group(3)
				date = re_result.group(4)
				message = re_result.group(5)
				#Remove newlines from all messages and the 'OK' AT command from the last message.
				if text_array_index == len(text_array) - 1:
					#'.*' at end removes +Class0 status messages (we hope).
					message = re.sub('[\r\n]+OK\r\n.*$', '', message)
				else:
					message = re.sub('[\r\n]+$', '', message)
				#Put each SMS in message array.
				sms_obj = SMS(index, status, phone, date, message)
				sms_array.append(sms_obj)
		return sms_array
	
	#Deletes text with specified index from SIM card.			
	def delete_text(self, index):
		if self.__does_message_at_index_exist(index):
			command = 'AT+CMGD=' + index
			self.send_AT(command)
			if self.__does_message_at_index_exist(index):
				return "text at index '" + index + "' not deleted"
			else:
				return "text at index '" + index + "' deleted"
		else:
			return "text at index '" + index + "' not found"
		
	#Probes SIM card to see if message at index exists.
	def __does_message_at_index_exist(self, index):
		sms_list = self.get_all_texts()
		for sms in sms_list:
			if sms.index == index:
				return 1
		return 0

	#Saves array of SMS objects to json file.
	def save_sms_obj_to_json_file(self, text_array, filename):
		if self.__is_sms_array(text_array):
			#Create dictionary (hashlike structure)
			data = {}
			#Create an array 
			data['sms'] = []
			for sms in text_array:
				data['sms'].append({
					'index': sms.index,
					'status': sms.status,
					'phone': sms.phone,
					'date': sms.date,
					'message': sms.message
				})
			outfile = open(filename, 'w')
			json.dump(data, outfile)
			outfile.close()
	
	#Returns array of SMS message objects taken from json file.
	def json_file_to_sms_array(self, filename):
		json_file = open(filename, 'r')
		read_data = json.load(json_file)
		json_file.close()
		sms_array = []
		for sms_json in read_data['sms']:
			sms_obj = SMS(sms_json['index'], sms_json['status'], sms_json['phone'], sms_json['date'], sms_json['message'])
			sms_array.append(sms_obj)
		return sms_array

	def append_texts_to_db_file(self, sms_array, sms_database_file):
		if self.__is_sms_array(sms_array):
			#Write new sms messages to database.
			#First check if sms database file exists.
			try:
				open(sms_database_file)
			#If doesn't exist create it and write new sms messages to it.
			except IOError:
				self.save_sms_obj_to_json_file(sms_array, sms_database_file)
			#Otherwise, read text from database and append sms_array and save to file.
			else:
				db_sms_array = self.json_file_to_sms_array(sms_database_file)
				full_db_sms_array = db_sms_array + sms_array 
				self.save_sms_obj_to_json_file(full_db_sms_array, sms_database_file)

	def delete_texts_from_sim_card(self, sms_array):
		if self.__is_sms_array(sms_array):
			for sms in sms_array:
				self.delete_text(sms.index)

	#Do we have an array containing SMS objects
	def __is_sms_array(self, sms_array):
		if len(sms_array) > 0:
			for sms in sms_array:
				if not isinstance(sms, SMS):
					raise Exception("The objects in the inputted array are not SMS objects!")
			#Array has elements, and those elements are SMS objects.
			return 1

class SMS:
		def __init__(self, index, status, phone, date, message):
		#def __init__(self, index):
			self.index = index
			self.status	= status 
			self.phone = phone
			self.date = date
			self.message = message




