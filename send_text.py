#!/usr/bin/python
import time
import serial
import re

# configure the serial connections (the parameters differs on the device you are connecting to)
ser = serial.Serial(
    port='/dev/ttyUSB2',
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_TWO,
    bytesize=serial.EIGHTBITS
)

#Send AT command to modem.
def send_AT(AT):
    ser.isOpen()   
    ser.write(AT + "\r\n")
    time.sleep(1)
    ser_response = '';
    while ser.inWaiting() > 0:
        ser_response += ser.read(1)
    return ser_response

#Check if SIM card configured for SMS text mode.
def check_sms_mode():
    sms_mode = send_AT('AT+CMGF?')
    regex_mode_result = re.search("\+CMGF:\s+([01])", sms_mode)
    if regex_mode_result.group(1) == '1':
        return "text_mode_on"
    elif regex_mode_result.group(1) == '0':
        return "text_mode_off"
    else:
        return "text_mode_error"

#Set SMS for text mode. sms_mode of 1 = texting (this is what we want), 0 = Programmable data unit PDU.
def set_sms_mode(sms_mode):
    sms_mode = str(sms_mode) #convert num to string
    sms_mode_response = send_AT('AT+CMGF=' + sms_mode)
    ok = re.findall("OK", sms_mode_response)
    if (not ok):
        raise Exception("SMS mode ", sms_mode, " was not successfully set\n")

def send_text(number, message):
    #Make sure texting is turned on in the SIM card.
    current_sms_mode = check_sms_mode()
    if current_sms_mode == "text_mode_off":
        set_sms_mode("1")
    elif current_sms_mode == "text_mode_error":
        raise Exception("SMS mode query error. There may be a problem with modem communication.")
    #Send the modem the CMGS command in the format to send a text out, where chr(26) is the required ctrl+Z that denotes EOF
    response1 = send_AT('AT+CMGS="' + number + '"\r\n') 
    response2 = send_AT( message + chr(26))
    #time.sleep(3)
    #response3 = send_AT('\r\n')
    #print ('AT+CMGS="' + number + '"\r\n' + message + chr(26))
    print "CMGS response1: ", response1, "\n"
    print "CMGS response2: ", response2, "\n"
    #print "CMGS response3: ", response3, "\n"

send_text("5033803136", "hi len this is send_text()")


#response_sendtext = send_AT('AT+CMGS="' + '5039895540"' + "\r\n" + "test python send_text" + chr(26))
#print ("response to sending text:" + response_sendtext)

