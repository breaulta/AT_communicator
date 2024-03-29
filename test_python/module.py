#!/usr/bin/python
# -*- coding: utf-8 -*-
#Without the previous 'coding' line, the gsm/ext mapping won't work with python 2.7
import time
import serial		#Works on Len's pi. Looks like it's a tough, depreciated package otherwise.
import re
import json
import os

#Import pgsmm functionality
from gsmmodem.modem import GsmModem

#GSM-7 mapping. https://en.wikipedia.org/wiki/GSM_03.38
gsm = (u"@£$¥èéùìòÇ\nØø\rÅåΔ_ΦΓΛΩΠΨΣΘΞ\x1bÆæßÉ !\"#¤%&'()*+,-./0123456789:;<=>"
   u"?¡ABCDEFGHIJKLMNOPQRSTUVWXYZÄÖÑÜ`¿abcdefghijklmnopqrstuvwxyzäöñüà")
ext = (u"````````````````````^```````````````````{}`````\\````````````[~]`"
   u"|````````````````````````````````````€``````````````````````````")

class Transmitter:
	#Initalize Transmitter object attributes.
	def __init__(self, port='/dev/ttyUSB2', qmi_path='/dev/cdc-wdm0', baud='115200', **kwargs):
		#Ensure that we're running as root.
		if not os.geteuid()==0:
			raise Exception("Must run as root!")
		self.ensure_sim_card_connected_to_network(qmi_path)
		#self._configure_ser_connection_to_usb(self.usb_path)
		#self._connect_to_modem(port, baud, qmi_path)
		#Globals for Concatenated Short Messages (PDU)
		self.message_ref = 0x00
		self.CSM_ref = 0x00

	#Add pgsmm modem connection
	#May be necessary to catch timeout issues. Waiting on this till someone can manually reset if needed.
	def _connect_to_modem(self, port, baud, qmi_path):
		self.modem = GsmModem(port, baud)
		print("connecting...")
		self.modem.connect()
		#This doesn't seem to work properly
		#Brig notes: try to del the object
		#try:
		#	self.modem.connect()
		#except:
		#	print('caught timeout error!')
		#	del self.modem
		#	self._reset_sim_hat(qmi_path)
		#	self._connect_to_modem(port, baud, qmi_path)
			#self.modem = GsmModem(port, baud)
			#self.modem.connect()
		print('outside try')

	#Check that the SIM card via the Qmicli interface is connected to the mobile network.
	#Default for raspberry pi + waveshare SIM7600 Hat is /dev/cdc-wdm0
	#Must run as root
	def ensure_sim_card_connected_to_network(self, sim_path):
		#Check if our SIM card is connected to the network or not.
		sim_mode = self._get_qmicli_mode(sim_path)
		#If not online, try to turn it on.
		if sim_mode != "online":
			#If sim/modem is reset when the serial connection is open, it will clobber /dev/ttyUSB2.
			#So we close the serial connection while we perform the reset.
			#if self.ser.isOpen() == True:
			#	self.ser.close()
			#print "Sim card was off, turning online."
			self._set_qmicli_mode('online', sim_path)
			timeout_count = 0
			#Verify that it comes online.
			while(1):
				time.sleep(10)
				sim_mode = self._get_qmicli_mode(sim_path)
				if sim_mode == 'online':
					#We're online! Escape bonds of while loop and return.
					print "Successfuly set sim card online."
					break
				#Otherwise, let's try to turn it online.
				else:
					print "Sim card is being reset to turn it online."
					time.sleep(10)
					self._set_qmicli_mode('reset', sim_path)
					time.sleep(30)
					#For potential debugging. We expect SIM mode = 'low-power' here after reset.
					get_response = self._get_qmicli_mode(sim_path)
					if 'low-power' != get_response:
						print "Warning, SIM Mode is: " + get_response
					else:
						print "We're in low power mode, please wait as we turn SIM online."
					time.sleep(1)
					self._set_qmicli_mode('online', sim_path)
					time.sleep(20)
					timeout_count += 1
					#Time out after a few minutes of trying
					if timeout_count > 2:
						raise Exception("The SIM card could not be set to online mode!")
			#Turn serial connection back on after resetting sim/modem.
			#self._configure_ser_connection_to_usb(self.usb_path)
			return 1
		#Looks like we're online! Return true.
		else:
			return 1

	def _reset_sim_hat(self, sim_path):
		#set offline
		self._set_qmicli_mode('reset', sim_path)
		time.sleep(5)
		#then call ensure_sim_connected
		self.ensure_sim_card_connected_to_network(sim_path)

	#Check to make sure the sim_path exists, which implies that the modem can accept qmicli commands
	def _check_sim_path(self, sim_path):
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
	def _set_qmicli_mode(self, mode, sim_path):
		self._check_sim_path(sim_path)
		os.system("qmicli -d " + sim_path + " --dms-set-operating-mode='" + mode + "'")
	
	#Returns SIM card mode (e.g. 'offline', 'online', 'low-power', 'reset', etc.
	def _get_qmicli_mode(self, sim_path):
		self._check_sim_path(sim_path)
		get_output = os.popen('qmicli -d ' + sim_path + ' --dms-get-operating-mode')
		output_read = get_output.read()
		mode_match = re.search("Mode: '([a-z-]+)'", output_read)
		if mode_match.group(1) is not None:
			return mode_match.group(1)
		else:
			print "Error: we could not read mode for:\n" + output_read
			return 0

	#remove
	#Send AT command to modem using pgsmm.
	def send_AT(self, modem, AT):
		prune = modem.write(AT, timeout=5, expectedResponseTermSeq='> ') # WRONG 
		#print('at: ', AT)
		print('raw return from modem.write: ', prune)
		response = re.search("\[u'(.+)'\]", str(prune))
		#print(response.group(1))
		return response.group(1)

	#Remove this probably
	#Check if SIM card configured for SMS text mode.
	def check_sms_mode(self):
		at_command = 'AT+CMGF?'
		sms_mode = self.modem.write(at_command, timeout=5)
		print 'sms_mode:'
		print sms_mode[0]
		regex_mode_result = re.search("\+CMGF:\s+([01])", sms_mode[0])
		print regex_mode_result
		if regex_mode_result:
			#If CMGF = 1, our sim is in text mode
			if regex_mode_result.group(1) == '1':
				return "text_mode_on"
			#If CMGF = 0, our sim is in pdu mode
			elif regex_mode_result.group(1) == '0':
				return "text_mode_off"
		#We ran into this bug once before, hopefully we can narrow it down with this exception:
		raise Exception("Error: our CMGF query didn't return 1 or 0, here's what we got back: ~" + sms_mode + "~")

	#Needed for long text
    #Set SMS for text mode. sms_mode of 1 = texting (this is what we want), 0 = Programmable data unit PDU.
	def set_sms_mode(self, modem, sms_mode):
		sms_mode = str(sms_mode) #convert num to string
		sms_mode_response = self.send_AT(modem, 'AT+CMGF=' + sms_mode)
		print ("sms mode response: " + sms_mode_response)
		ok = re.findall("OK", sms_mode_response)
		if (not ok):
			raise Exception("SMS mode ", sms_mode, " was not successfully set\n")

	#Original function source: https://guiott.com/GSMcontrol/Python_GSM/_modules/gsmmodem/pdu.html
	#Given a bytearray of octets, pack into septets and return a bytearray of them.
	def packSeptets(self, octets, padBits=6):
		result = bytearray()
		#Make the array iteratable. I think this allows the for loop to work on a bytearray.
		octets = iter(octets)
		shift = padBits
		#zeros need to be shifted in from prevSeptet in order to insert padding bits.
		prevSeptet = 0x00
		for octet in octets:
			#For septet packing we do a bitwise and with the 7 least sig digits.
			septet = octet & 0x7f;	
			if shift == 7:
				# prevSeptet has already been fully added to result
				shift = 0
				prevSeptet = septet
				continue
			#Bitmagic septet packing. An explaination for septet packing can be found here:
			# https://www.codeproject.com/Tips/470755/Encoding-Decoding-7-bit-User-Data-for-SMS-PDU-PDU
			b = ((septet << (7 - shift)) & 0xFF) | (prevSeptet >> shift)
			prevSeptet = septet
			shift += 1
			result.append(b)
		if shift != 7:
			# There is a bit "left over" from prevSeptet
			result.append(prevSeptet >> shift)
		return result

	#Convert a string of characters to GSM7 encoded bytearray.
	#Original function source: https://guiott.com/GSMcontrol/Python_GSM/_modules/gsmmodem/pdu.html
	def encode_gsm_octets(self, plaintext):
		if type(plaintext) != str:
			 plaintext = str(plaintext)
		result = bytearray()
		#Make sure chars are in utf-8 format.
		for c in plaintext.decode('utf-8'):
			#The index corresponds to the gsm7 number(int/hex/binary) representation.
			idx = gsm.find(c)
			if idx != -1:
				result.append(idx)
			else:
				idx = ext.find(c)
				if idx != -1:
					result.append(27)
					result.append(idx)
		return result

	#Original function source: https://guiott.com/GSMcontrol/Python_GSM/_modules/gsmmodem/pdu.html
	#Divides a long text that needs to be broken up and sent via PDU. Some GSM7 chars are 2 bytes long, 
	# so this function makes sure that the converted octet length doesn't exceed 153.
	def divide_text(self, plainText):
		result = []
		plainStartPtr = 0
		plainStopPtr  = 0
		chunkByteSize = 0
		while plainStopPtr < len(plainText):
			char = plainText[plainStopPtr]
			idx = gsm.find(char)
			if idx != -1:
				chunkByteSize = chunkByteSize + 1;
			elif char in ext:
				chunkByteSize = chunkByteSize + 2;
			else:
				raise ValueError('Cannot encode char "{0}" using GSM-7 encoding'.format(char))
			plainStopPtr = plainStopPtr + 1
			if chunkByteSize > 153:
				plainStopPtr = plainStopPtr - 1
			if chunkByteSize >= 153:
				result.append(plainText[plainStartPtr:plainStopPtr])
				plainStartPtr = plainStopPtr
				chunkByteSize = 0
		if chunkByteSize > 0:
			result.append(plainText[plainStartPtr:])
		return result

	#Converts a number string into the reverse nibble, Binary Coded Decimal bytearray needed for Concatenated Short Message.
	def convert_to_DA(self, number):
		if len(number) == 10:
			destination_address = '1' + number
		elif len(number) == 11:
			destination_address = number
		else:
			raise Exception("Failed to convert to Destination Address: input has the wrong number of digits!")
		#F indicates the end of the Destination Address.
		destination_address = destination_address + 'F'
		result = bytearray()
		#From 0 to the length of the DA, count i by 2.
		for i in xrange(0, len(destination_address), 2):
			#(Take slice from i to (i+2)-1 [i:i+2]) (and reverse it [::-1])
			octet = destination_address[i:i+2][::-1]
			#Convert the 16 bit octet string into a number.
			number = int(octet, 16)
			result.append(number)
		return result

	#Send a series of Concatenated Short Messages in PDU mode. The recipient's phone (Terminal Equipment) will re-assemble.
	#Function composed from SMS/Octet map in a way that is easy to read, walk through.
	def send_long_text(self, modem, number, message):
		number = re.sub(r'^\+', '', number)
		self.set_sms_mode(modem, '0')				#Set modem to PDU mode.
		service_center_address = 0x00		#Value of 00 tells the modem to use the default address.
		#1 in the least sig bit indicates SMS-SUBMIT. 1 in the 7th least sig bit indicates the presence of the User Data Header.
		#b 0100 0001 = 0x41
		message_type_indicator = 0x41
		#self.message_ref					#Counts up for each pdu short message we send.
		DA_len = 0x0B						#Indicates the length of the Destination Address.
		number_plan_ID = 0x91				#Indicates how to interpret the DA
		destination_address = self.convert_to_DA(number)	#Reverse nibble, Binary Coded Decimal, ending with F.
		protocol_ID = 0x00					#Value of 00 indicates a 'normal SMS'
		data_coding_scheme = 0x00			#Value of 00 indicates that the payload will be coded in GSM-7.
		user_data_length = 0x00				#Length of the payload in septets.
		user_data_header_length = 0x05		#A static 5 octets will be the length of the UDH for our CSM usage.
		information_element_identifier = 0x00	#Value of 00 indicates that this IE will be a CSM header.
		IEI_length = 0x03						#The IE will be 3 octets long.
		#self.CSM_ref							#Unique identifier for Concatenated Short Message group.
		total_CSM_parts = 0x00					#Number of parts of the CSM group.
		CSM_sequence_number = 0x01				#The current iteration of the part (starting with 1).
		user_data = bytearray()					#GSM-7 encoded payload data.

		message_list_pdu = []
		#divide the long text into segments that won't cause errors (hex length <= 153), keeping the extended alphabet in mind.
		message_list_pdu = self.divide_text(message)
		total_CSM_parts = len(message_list_pdu)
		pdus = []
		#Line up the bytes of each part and send it.
		for SM_part in message_list_pdu:
			pdu = bytearray()
			octets = self.encode_gsm_octets(SM_part)		#byte array
			#(One of the) Fill bits calculation:
			#UDHL+IEI+IEIL+CSM_ref+total_CSM_parts+CSM_sequence_number = 6 octets
			#number of septets + 7: (49/7 = 7) 6 octets of bits = 48. Need 1 bit to get to 49 which is divisible by 7.
			user_data_length = len(octets) + 7
			print "udl = " + str(user_data_length)
			user_data = self.packSeptets(octets)	#byte array
			pdu.append(service_center_address)
			pdu.append(message_type_indicator)
			pdu.append(self.message_ref)
			self.message_ref += 1
			pdu.append(DA_len)
			pdu.append(number_plan_ID)
			#Extend is used to concatenate arrays.
			pdu.extend(destination_address)
			pdu.append(protocol_ID)
			pdu.append(data_coding_scheme)
			pdu.append(user_data_length)
			pdu.append(user_data_header_length)
			pdu.append(information_element_identifier)
			pdu.append(IEI_length)
			pdu.append(self.CSM_ref)
			pdu.append(total_CSM_parts)
			pdu.append(CSM_sequence_number)
			CSM_sequence_number += 1
			pdu.extend(user_data)
			#Don't count the service_center_address as it is not part of the PDU protocol layer.
			pdu_length = str(len(pdu) - 1)
			print("AT length: " + pdu_length)
			print("SM part " + str(CSM_sequence_number - 1) + ":")
			pdu_string = ''
			#Python likes to remove preceeding zeros from hex numbers. This makes sure the zeros are not removed.
			for byte in pdu:
				#If there are fewer than 2 digits, fill with up to 2 zeros.
				pdu_string += hex(byte)[2:].zfill(2)
			print(pdu_string)
			#Send the modem the CMGS command in the format to send a text out, where \x1a is the required ctrl+Z that denotes EOF
			CMGS = 'AT+CMGS=' + pdu_length
			response1 = modem.write(CMGS, timeout=5, expectedResponseTermSeq='> ') #, waitForResponse=False)
			response2 = modem.write( pdu_string, timeout=100, writeTerm='\x1a')

		#After the set of Concatenated Short Messages finishes, increment so the next group gets a different ref number.
		self.CSM_ref += 1
	
	#Replace with pgsmm version
	#add perameter for 'spy' and 'flash' texts
	def send_text(self, number, message):
		print('enter send text')

		self.set_sms_mode('1')#Set modem to text mode. pgsmm might do this automatically.
		#Make sure texting is turned on in the SIM card.
		current_sms_mode = self.check_sms_mode()
		if current_sms_mode == "text_mode_off":
			self.set_sms_mode("1")
		elif current_sms_mode == "text_mode_error":
			raise Exception("SMS mode query error. There may be a problem with modem communication.")
		
		#response1 = self.send_AT('AT+CMGS="' + number + '"') # + '"\r\n')
		AT = 'AT+CMGS="' + number + '"'
		response1 = self.modem.write(AT, timeout=5, expectedResponseTermSeq='> ') #, waitForResponse=False)
		print('resp1')
		print(response1)
		time.sleep(1)
		#writeterm is the termination character
		response2 = self.modem.write( message, timeout=100, writeTerm='\x1a')
		print('resp2')
		print(response2)

	#pgsmm will replace
	#Returns array of SMS objects, returning all texts on SIM card.
	def get_all_texts(self):
		sms_array = []
		#self.set_sms_mode('1')
		#text_list = self.send_AT('AT+CMGL="ALL"')
		#AT = 'AT+CMGL="ALL"'
		#text_list = self.modem.write(AT, timeout=5, expectedResponseTermSeq='+CMGL:')

		smslist = self.modem.listStoredSms(4, memory=None, delete=False)
		return smslist

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
	
	#pgsmm will replace
	#Deletes text with specified index from SIM card.			
	def delete_text(self, index):
		if self._does_message_at_index_exist(index):
			command = 'AT+CMGD=' + index
			self.send_AT(command)
			if self._does_message_at_index_exist(index):
				return "text at index '" + index + "' not deleted"
			else:
				return "text at index '" + index + "' deleted"
		else:
			return "text at index '" + index + "' not found"
		
	#replace
	#Probes SIM card to see if message at index exists.
	def _does_message_at_index_exist(self, index):
		sms_list = self.get_all_texts()
		for sms in sms_list:
			if sms.index == index:
				return 1
		return 0

	#replace
	#Saves array of SMS objects to json file.
	def save_sms_obj_to_json_file(self, text_array, filename):
		if self._is_sms_array(text_array):
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

	#remove	
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
		if self._is_sms_array(sms_array):
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

	#remove
	def delete_texts_from_sim_card(self, sms_array):
		if self._is_sms_array(sms_array):
			for sms in sms_array:
				self.delete_text(sms.index)

	#remove
	#Do we have an array containing SMS objects
	def _is_sms_array(self, sms_array):
		if len(sms_array) > 0:
			for sms in sms_array:
				if not isinstance(sms, SMS):
					raise Exception("The objects in the inputted array are not SMS objects!")
			#Array has elements, and those elements are SMS objects.
			return 1

class SMS:
		def __init__(self, phone, date, message, index=None, status=None):
		#def __init__(self, index):
			self.index = index
			self.status	= status 
			self.phone = phone
			self.date = date
			self.message = message




