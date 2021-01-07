#!/usr/bin/env python
# -*- coding: utf-8 -*-

gsm = (u"@£$¥èéùìòÇ\nØø\rÅåΔ_ΦΓΛΩΠΨΣΘΞ\x1bÆæßÉ !\"#¤%&'()*+,-./0123456789:;<=>"
   u"?¡ABCDEFGHIJKLMNOPQRSTUVWXYZÄÖÑÜ`¿abcdefghijklmnopqrstuvwxyzäöñüà")
ext = (u"````````````````````^```````````````````{}`````\\````````````[~]`"
   u"|````````````````````````````````````€``````````````````````````")

def packSeptets(octets, padBits=6):
    
    result = bytearray()
    octets = iter(octets)
    shift = padBits
	#Hardcoding padBits = 6, zeros need to be shifted in from prevSeptet.
    prevSeptet = 0x00
    for octet in octets:
        septet = octet & 0x7f;
        if shift == 7:
            # prevSeptet has already been fully added to result
            shift = 0
            prevSeptet = septet
            continue
        b = ((septet << (7 - shift)) & 0xFF) | (prevSeptet >> shift)
        prevSeptet = septet
        shift += 1
        result.append(b)
        #print hex(b)
    if shift != 7:
        # There is a bit "left over" from prevSeptet
        result.append(prevSeptet >> shift)

    return result

def getBytes(plaintext):
    if type(plaintext) != str:
         plaintext = str(plaintext)
    #bytes = []	# Is bytes a special python list?
    result = bytearray()
    for c in plaintext.decode('utf-8'):
        idx = gsm.find(c)
        if idx != -1:
            result.append(idx)
        else:
            idx = ext.find(c)
            if idx != -1:
                result.append(27)
                result.append(idx)
    return result 

def gsm_pack_and_encode(plaintext):
	octets = getBytes(plaintext)
	septets = packSeptets(octets)
	text = []
	for septet in septets:
		#print hex(septet)
		text.append(chr(septet).encode('hex').upper())
	return text

def get_encode(currentByte, index, bitRightCount, position, nextPosition, leftShiftCount, bytesLength, bytes):
    if index < 8:
        byte = currentByte >> bitRightCount
        if nextPosition < bytesLength:
            idx2 = bytes[nextPosition]
            byte = byte | ((idx2) << leftShiftCount)
            byte = byte & 0xFF
        else:
            byte = byte & 0xFF
        return chr(byte).encode('hex').upper()
    return ''

def gsm_encode(plaintext):
    res = ""
    f = -1
    t = 0
    bytes = getBytes(plaintext)
    bytesLength = len(bytes)
    for b in bytes:
        f = f+1
        t = (f%8)+1
        res += get_encode(b, t, t-1, f, f+1, 8-t, bytesLength, bytes)

    return res


def chunks(l, n):
    if n < 1:
        n = 1
    return [l[i:i + n] for i in range(0, len(l), n)]

def gsm_decode(codedtext):
    hexparts = chunks(codedtext, 2)
    number   = 0
    bitcount = 0
    output   = ''
    found_external = False
    for byte in hexparts:
        byte = int(byte, 16);
        # add data on to the end
        number = number + (byte << bitcount) #left shift (<<) adds a preceeding zero
        # increase the counter
        bitcount = bitcount + 1
        # output the first 7 bits
        if number % 128 == 27:	# Using mod of 128 to overflow after 7 bits.
             '''skip'''
             found_external = True
        else:
            if found_external == True:                
                 character = ext[number % 128]
                 found_external = False
            else:
                 character = gsm[number % 128]
            output = output + character

        # then throw them away
        number = number >> 7
        # every 7th letter you have an extra one in the buffer
        if bitcount == 7:
            if number % 128 == 27:
                '''skip'''
                found_external = True
            else:
                if found_external == True:                
                    character = ext[number % 128]
                    found_external = False
                else:
                    character = gsm[number % 128]
                output = output + character

            bitcount = 0
            number = 0
    return output

#This method encodes a long (multipart) SMS in PDU format for an immediate send.  As it stands, the scope of this project 
#doesn't include using PDU format for anything but Concatenated SMS, so several pieces will be hardcoded.
#def pdu_encode(message, number):


#print (gsm_encode("Howdy y'all!"))
message = "Howdy y'all!"
#for c in message:
#	print gsm_encode(c)

#print gsm_encode("Hi Len~ how's it going?")
#print gsm_encode('jack and jill~ went up a hill() to fetch a pail of water!***')


#print (gsm_decode("C8f79D9C07E54F61363B04"))


print ( "".join(gsm_pack_and_encode("e eu fugiat nulla pariatur.Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.")))

print (gsm_encode("e eu fugiat nulla pariatur.Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."))

print (gsm_decode("6550B90E32D7CFE9301DE4AEB3D961103C2C4F87E975B9AB881F97E1F4725D0E9AA7DD74D07B3C0E97C7613A685C87A7C9617A980E72BFDD20B8FC9D2697DD7416685E77D3416937685C67C3C3A0783D0D7A9BCDE9713A0C2297E76579DD4D07B5DF6C769A0E0ABBD36D509A0C2ACFE9207658FC96D7DB2E"))

"""
encoded: 6550B90E32D7CFE9301DE4AEB3D961103C2C4F87E975B9AB881F97E1F4725D0E9AA7DD74D07B3C0E97C7613A685C87A7C9617A980E72BFDD20B8FC9D2697DD7416685E77D3416937685C67C3C3A0783D0D7A9BCDE9713A0C2297E76579DD4D07B5DF6C769A0E0ABBD36D509A0C2ACFE9207658FC96D7DB2E

payload = 'CAA0721D64AE9FD3613AC85D67B3C32078589E0ED3EB7257113F2EC3E9E5BA1C344FBBE9A0F7781C2E8FC374D0B80E4F93C3F4301DE47EBB4170F93B4D2EBBE92CD0BCEEA683D26ED0B8CE868741F17A1AF4369BD3E37418442ECFCBF2BA9B0E6ABFD9EC341D1476A7DBA03419549ED341ECB0F82DAFB75D'

print binascii.b2a_hex(hex(payload))

print (gsm_decode(binascii.b2a_hex(hex(payload))))
"""




