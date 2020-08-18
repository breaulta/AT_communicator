#!/usr/bin/python
import time
import serial
import re

class Transmitter:
	#Initalize Transmitter object attributes.
	def __init__(self, **kwargs):
		#If a specific port is specified, connect to that port.
		defined_port = ''
		if 'port' in kwargs:
			defined_port = kwargs['port']
		else:
			defined_port = '/dev/ttyUSB2'
	#Configure serial connection settings.
		self.ser = serial.Serial(
			port=defined_port,
			baudrate=9600,
			parity=serial.PARITY_NONE,
			stopbits=serial.STOPBITS_TWO,
			bytesize=serial.EIGHTBITS
		)

    #Send AT command to modem.
	def send_AT(self, AT):
		self.ser.isOpen()   
		self.ser.write(AT + "\r\n")
		time.sleep(1)
		ser_response = '';
		while self.ser.inWaiting() > 0:
			ser_response += self.ser.read(1)
		return ser_response

	#Check if SIM card configured for SMS text mode.
	def check_sms_mode(self):
		sms_mode = self.send_AT('AT+CMGF?')
		regex_mode_result = re.search("\+CMGF:\s+([01])", sms_mode)
		if regex_mode_result.group(1) == '1':
			return "text_mode_on"
		elif regex_mode_result.group(1) == '0':
			return "text_mode_off"
		else:
			return "text_mode_error"

    #Set SMS for text mode. sms_mode of 1 = texting (this is what we want), 0 = Programmable data unit PDU.
	def set_sms_mode(self, sms_mode):
		sms_mode = str(sms_mode) #convert num to string
		sms_mode_response = self.send_AT('AT+CMGF=' + sms_mode)
		ok = re.findall("OK", sms_mode_response)
		if (not ok):
			raise Exception("SMS mode ", sms_mode, " was not successfully set\n")

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
		time.sleep(3)
		response3 = self.send_AT('\r\n')
		print "CMGS response1: ", response1, "\n"
		print "CMGS response2: ", response2, "\n"
		print "CMGS response3: ", response3, "\n"

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
					message = re.sub('[\r\n]+OK\r\n$', '', message)
				else:
					message = re.sub('[\r\n]+$', '', message)
				#Put each SMS in message array.
				sms_obj = SMS(index, status, phone, date, message)
				sms_array.append(sms_obj)
		return sms_array
				
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
		

	def _does_message_at_index_exist(self, index):
		sms_list = self.get_all_texts()
		for sms in sms_list:
			if sms.index == index:
				return 1
		return 0


class SMS:
	def __init__(self, index, status, phone, date, message):
	#def __init__(self, index):
		self.index = index
		self.status	= status 
		self.phone = phone
		self.date = date
		self.message = message


