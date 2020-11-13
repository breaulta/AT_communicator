import time
import serial

# configure the serial connections (the parameters differs on the device you are connecting to)
ser = serial.Serial(
    port='/dev/ttyUSB2',
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_TWO,
    bytesize=serial.EIGHTBITS
)

#from brig: maybe add a queue to handle responses from the modem. could also set up a function to do something on the return a la node.


ser.isOpen()

print 'Enter your commands below.\r\nInsert "exit" to leave the application.'

send=1
for send in ['AT','AT+CMGF?']*5 :
    # get keyboard send
    # send = raw_input(">> ")
    #     # Python 3 users
    #     # input = input(">> ")
    # if input == 'exit':
    #     ser.close()
    #     exit()
    #else:
	# send the character to the device
	# (note that I happend a \r\n carriage return and line feed to the characters - this is requested by my device)
	ser.write(send + '\r\n')
	out = ''
	# let's wait one second before reading output (let's give device time to answer)
	while ser.inWaiting() > 0:
		out += ser.read(1)

	if out != '':
            print ">>" + out
	else:
		print '.', 
