import sys
import unicodedata
import binascii

message = 'hello world'
hex_message = ''
for c in message:
	#removes the first 2 digits
	hex_message += hex(ord(c))[2:]

print hex_message

print binascii.b2a_hex(message)



uni = u'\u054c'
print uni
print repr(uni)

exit(0)
message = 'hello world'
print('orig: ' + message)
bytes(message)
unicoded = unicode(message, 'utf-8')

decoded = unicoded.decode('utf-8')
print decoded
print repr(decoded)



exit(0)
sys.stdout.write(repr(u.encode('utf-8')))
encoded = decoded.encode('ascii')
sys.stdout.write(repr('encoded: ' + encoded))
#sys.stdout.buffer.write(encoded)
#decoded = encoded.decode('utf-8')
#sys.stdout.buffer.write(decoded)

