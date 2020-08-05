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

#Set SMS for text mode.
def set_sms_mode(sms_mode):
    sms_mode_response = send_AT('AT+CMGF=' + sms_mode)
    ok = re.findall("OK", sms_mode_response)
    if (ok):
        print "it's ok\n"
    else:
        print "it's not ok\n"

#def send_text(number, message):

current_sms_mode = check_sms_mode()
if current_sms_mode == "text_mode_off":
    set_sms_mode("1")
elif current_sms_mode == "text_mode_error":
    #throw error
    raise Exception("SMS mode query error. There may be a problem with modem communication.")
response_sendtext = send_AT('AT+CMGS="' + '5039895540"' + "\r\n" + "test python send_text" + chr(26))
print ("response to sending text:" + response_sendtext)

exit(0)


if x:
  print("YES! We have a match x.group()!", x.group(1))

print "hey\n"
exit(0)
print "hello\n"

ser.write('AT+CMGS="5039895540"' + "\r\n" + "this is the message" + chr(26))
time.sleep(1)
out = ''
while ser.inWaiting() > 0:
    out += ser.read(1)
if out != '':
    print ">>>" + out

