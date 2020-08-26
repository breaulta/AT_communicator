#!/usr/bin/python

try:
	f = open("fake.txt")
except IOError:
	print "we caught it\n"	
